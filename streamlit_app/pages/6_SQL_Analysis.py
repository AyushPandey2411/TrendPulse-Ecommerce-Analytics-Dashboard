"""pages/6_SQL_Analysis.py"""
import os, sys
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APP_DIR)

import streamlit as st
import plotly.express as px
import sqlite3
import pandas as pd
from data_engine import load_and_process

st.set_page_config(page_title="SQL Analysis", page_icon="🗄️", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0f0f1f,#1a0a2e);border-right:1px solid #2d2d4e;}
[data-testid="stSidebar"] *{color:#c8c8e8 !important;}
.section-header{font-size:1.1rem;font-weight:600;color:#e0e0ff;border-left:3px solid #e94560;padding-left:12px;margin:24px 0 14px 0;}
.sql-box{background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:16px 20px;
         font-family:'JetBrains Mono',monospace;font-size:0.82rem;color:#79c0ff;
         white-space:pre;overflow-x:auto;margin:8px 0 16px 0;line-height:1.6;}
.badge{background:#e9456033;color:#e94560;padding:2px 10px;border-radius:12px;
       font-size:0.75rem;font-weight:600;margin-left:8px;}
</style>""", unsafe_allow_html=True)

st.markdown("## 🗄️ SQL Analysis")
st.caption("5 real business queries executed via SQLite in-memory — demonstrating SQL skills for DA/BA roles")

with st.spinner("Loading data into SQLite..."):
    df = load_and_process()
    conn = sqlite3.connect(":memory:")
    df_sql = df.copy()
    df_sql["order_month"] = df_sql["order_month"].astype(str)
    df_sql["age_group"]   = df_sql["age_group"].astype(str)
    df_sql.to_sql("transactions", conn, index=False, if_exists="replace")

st.success("✅ 50,000 rows loaded into in-memory SQLite database")

# ── Query selector ────────────────────────────────────────────────────────────
QUERIES = {
    "Q1 — Monthly Revenue + AOV": {
        "desc": "Aggregates revenue, order count, unique customers, and average order value by month. Classic GROUP BY + aggregate.",
        "sql": """SELECT
    order_month,
    ROUND(SUM(purchase_amount), 2)                                    AS revenue,
    COUNT(DISTINCT transaction_id)                                     AS orders,
    COUNT(DISTINCT user_name)                                          AS unique_customers,
    ROUND(SUM(purchase_amount) / COUNT(DISTINCT transaction_id), 2)   AS avg_order_value
FROM transactions
GROUP BY order_month
ORDER BY order_month""",
        "chart": "line"
    },
    "Q2 — Category % Contribution (Window Function)": {
        "desc": "Uses SUM() OVER() window function to calculate each category's % share of total revenue. Tests window function knowledge.",
        "sql": """SELECT
    product_category,
    ROUND(SUM(purchase_amount), 2)                                  AS revenue,
    COUNT(DISTINCT transaction_id)                                   AS orders,
    ROUND(100.0 * SUM(purchase_amount) /
          SUM(SUM(purchase_amount)) OVER (), 2)                     AS revenue_pct,
    ROUND(AVG(purchase_amount), 2)                                  AS avg_order_value
FROM transactions
GROUP BY product_category
ORDER BY revenue DESC""",
        "chart": "bar"
    },
    "Q3 — Top 20 Customers by Lifetime Value": {
        "desc": "Ranks customers by total spend with purchase history dates. Classic customer value ranking query.",
        "sql": """SELECT
    user_name,
    COUNT(DISTINCT transaction_id)   AS total_orders,
    ROUND(SUM(purchase_amount), 2)   AS lifetime_spend,
    ROUND(AVG(purchase_amount), 2)   AS avg_order,
    MIN(transaction_date)            AS first_purchase,
    MAX(transaction_date)            AS last_purchase
FROM transactions
GROUP BY user_name
ORDER BY lifetime_spend DESC
LIMIT 20""",
        "chart": "bar"
    },
    "Q4 — Payment Method Revenue Share": {
        "desc": "Compares payment methods by revenue, transaction count, AOV, and share percentage. Uses subquery for denominator.",
        "sql": """SELECT
    payment_method,
    COUNT(*)                                                          AS transactions,
    ROUND(SUM(purchase_amount), 2)                                    AS revenue,
    ROUND(AVG(purchase_amount), 2)                                    AS avg_order,
    ROUND(100.0 * COUNT(*) /
          (SELECT COUNT(*) FROM transactions), 2)                    AS txn_share_pct
FROM transactions
GROUP BY payment_method
ORDER BY revenue DESC""",
        "chart": "bar"
    },
    "Q5 — Country × Category Revenue Matrix": {
        "desc": "Cross-tab of country vs category revenue. Pivoted for matrix view — useful for identifying market-specific opportunities.",
        "sql": """SELECT
    country,
    product_category,
    ROUND(SUM(purchase_amount), 2)  AS revenue,
    COUNT(*)                         AS orders
FROM transactions
GROUP BY country, product_category
ORDER BY country, revenue DESC""",
        "chart": "heatmap"
    },
}

selected_q = st.selectbox("Select a query to run", list(QUERIES.keys()))
q = QUERIES[selected_q]

st.markdown(f'<div class="section-header">{selected_q} <span class="badge">SQL</span></div>',
            unsafe_allow_html=True)
st.markdown(f"**What this query does:** {q['desc']}")

with st.expander("📋 View SQL", expanded=True):
    st.markdown(f'<div class="sql-box">{q["sql"]}</div>', unsafe_allow_html=True)

result = pd.read_sql(q["sql"], conn)
st.markdown(f"**Result:** {len(result):,} rows returned")
st.dataframe(result, width="stretch", hide_index=True)

# ── Chart ─────────────────────────────────────────────────────────────────────
if q["chart"] == "line" and "revenue" in result.columns:
    fig = px.line(result, x="order_month", y="revenue",
                  markers=True, color_discrete_sequence=["#e94560"])
    fig.update_layout(template="plotly_dark", height=320,
                      paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
                      yaxis=dict(tickprefix="$"), margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig, width="stretch")

elif q["chart"] == "bar":
    y_col = [c for c in ["revenue","lifetime_spend","transactions"] if c in result.columns][0]
    x_col = result.columns[0]
    fig = px.bar(result.head(10), x=x_col, y=y_col,
                 color_discrete_sequence=["#0f3460"],
                 text_auto=True)
    fig.update_layout(template="plotly_dark", height=320,
                      paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
                      margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig, width="stretch")

elif q["chart"] == "heatmap":
    pivot = result.pivot(index="country", columns="product_category", values="revenue").fillna(0)
    fig = px.imshow(pivot, color_continuous_scale="RdYlGn",
                    text_auto=".0f",
                    labels=dict(color="Revenue ($)"))
    fig.update_layout(template="plotly_dark", height=420,
                      paper_bgcolor="#0a0a14",
                      margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig, width="stretch")

conn.close()

# ── Skills note ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">SQL Concepts Demonstrated</div>',
            unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown("""
    | Concept | Query |
    |---|---|
    | GROUP BY + Aggregates | Q1, Q2, Q3, Q4 |
    | Window Function (SUM OVER) | Q2 |
    | Subquery | Q4 |
    """)
with c2:
    st.markdown("""
    | Concept | Query |
    |---|---|
    | DISTINCT COUNT | Q1, Q3 |
    | Multi-column GROUP BY | Q5 |
    | ORDER BY + LIMIT | Q3 |
    """)
