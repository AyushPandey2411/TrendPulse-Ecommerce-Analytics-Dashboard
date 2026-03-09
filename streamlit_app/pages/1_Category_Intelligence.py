"""
pages/1_Category_Intelligence.py
"""
import os, sys
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APP_DIR)

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from data_engine import get_category_stats, load_and_process

st.set_page_config(page_title="Category Intelligence", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
[data-testid="stSidebar"] { background: linear-gradient(180deg,#0f0f1f,#1a0a2e); border-right:1px solid #2d2d4e; }
[data-testid="stSidebar"] * { color: #c8c8e8 !important; }
.section-header { font-size:1.1rem; font-weight:600; color:#e0e0ff; border-left:3px solid #e94560; padding-left:12px; margin:24px 0 14px 0; }
.insight-box { background:#12122a; border:1px solid #2a2a4a; border-left:3px solid #f5a623; border-radius:8px; padding:12px 16px; margin:6px 0; font-size:0.86rem; color:#c8c8e0; }
</style>""", unsafe_allow_html=True)

st.markdown("## 📊 Category Intelligence")
st.caption("Revenue performance, AOV comparison, and seasonal demand patterns by product category.")

with st.spinner("Analysing categories..."):
    cat_stats, cat_quarter = get_category_stats()
    df = load_and_process()

# ── Filters ───────────────────────────────────────────────────────────────────
col_f1, col_f2 = st.columns([3, 1])
with col_f2:
    metric = st.selectbox("Sort by", ["Revenue", "Orders", "Avg Order Value"])
sort_col = {"Revenue": "revenue", "Orders": "orders", "Avg Order Value": "avg_order"}[metric]
cat_sorted = cat_stats.sort_values(sort_col, ascending=False)

# ── Row 1 ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Revenue & AOV by Category</div>',
            unsafe_allow_html=True)
c1, c2 = st.columns(2)

PALETTE = ["#e94560","#0f3460","#533483","#f5a623","#00b4d8","#90e0ef","#16213e","#caf0f8"]

with c1:
    fig = go.Figure(go.Bar(
        x=cat_sorted["revenue"], y=cat_sorted["product_category"],
        orientation="h",
        marker=dict(color=PALETTE[:len(cat_sorted)]),
        text=[f"${v/1000:.0f}K ({p:.1f}%)" for v, p in
              zip(cat_sorted["revenue"], cat_sorted["revenue_pct"])],
        textposition="inside",
        textfont=dict(color="white", size=11),
        hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>"
    ))
    fig.update_layout(
        title="Revenue by Category", template="plotly_dark", height=360,
        paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
        xaxis=dict(tickprefix="$", tickformat=",.0f"),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig, width="stretch")

with c2:
    cat_aov = cat_stats.sort_values("avg_order")
    fig2 = go.Figure(go.Bar(
        x=cat_aov["avg_order"], y=cat_aov["product_category"],
        orientation="h",
        marker_color="#533483",
        text=[f"${v:.0f}" for v in cat_aov["avg_order"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>AOV: $%{x:.2f}<extra></extra>"
    ))
    fig2.update_layout(
        title="Average Order Value by Category", template="plotly_dark", height=360,
        paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
        xaxis=dict(tickprefix="$"),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig2, width="stretch")

# ── Row 2 — Quarterly heatmap ─────────────────────────────────────────────────
st.markdown('<div class="section-header">Seasonal Demand — Quarterly Revenue Heatmap</div>',
            unsafe_allow_html=True)

import plotly.figure_factory as ff
z     = cat_quarter.values.tolist()
xlabs = [f"Q{q}" for q in cat_quarter.columns.tolist()]
ylabs = cat_quarter.index.tolist()
annot = [[f"${v/1000:.0f}K" for v in row] for row in z]

fig3 = ff.create_annotated_heatmap(
    z=z, x=xlabs, y=ylabs,
    annotation_text=annot,
    colorscale="YlOrRd", showscale=True
)
fig3.update_layout(
    template="plotly_dark", height=350,
    paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
    margin=dict(l=0, r=0, t=20, b=0),
    xaxis=dict(side="bottom")
)
st.plotly_chart(fig3, width="stretch")

# ── Row 3 — Treemap ───────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Revenue Share — Treemap</div>',
            unsafe_allow_html=True)

fig4 = px.treemap(
    cat_stats,
    path=["product_category"],
    values="revenue",
    color="avg_order",
    color_continuous_scale="RdBu",
    custom_data=["revenue_pct", "orders"]
)
fig4.update_traces(
    texttemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{customdata[0]:.1f}%",
    hovertemplate="<b>%{label}</b><br>Revenue: $%{value:,.0f}<br>Share: %{customdata[0]:.1f}%<br>Orders: %{customdata[1]:,}<extra></extra>"
)
fig4.update_layout(
    height=380, paper_bgcolor="#0a0a14",
    margin=dict(l=0, r=0, t=10, b=0)
)
st.plotly_chart(fig4, width="stretch")

# ── Insights ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Key Insights</div>', unsafe_allow_html=True)
top_cat = cat_stats.iloc[0]
low_cat = cat_stats.iloc[-1]
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""<div class="insight-box">
    🏆 <strong>{top_cat['product_category']}</strong> leads revenue at
    <strong>${top_cat['revenue']:,.0f}</strong> ({top_cat['revenue_pct']:.1f}% share).
    Expand assortment depth here first.</div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="insight-box">
    ⚖️ All 8 categories are within <strong>5% of each other</strong> in revenue —
    healthy catalogue diversification with no single dependency.</div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="insight-box">
    📦 Q4 shows the highest revenue across most categories — recommend
    <strong>15–20% inventory buffer</strong> for Electronics & Toys pre-Q4.</div>""",
    unsafe_allow_html=True)

# ── Data Table ────────────────────────────────────────────────────────────────
with st.expander("📋 Full Category Data Table"):
    display = cat_stats.copy()
    display["revenue"]     = display["revenue"].apply(lambda x: f"${x:,.0f}")
    display["avg_order"]   = display["avg_order"].apply(lambda x: f"${x:.2f}")
    display["revenue_pct"] = display["revenue_pct"].apply(lambda x: f"{x:.1f}%")
    st.dataframe(display, width="stretch", hide_index=True)
