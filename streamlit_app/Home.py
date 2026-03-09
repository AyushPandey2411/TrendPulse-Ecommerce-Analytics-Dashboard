"""
streamlit_app/Home.py
─────────────────────
TrendPulse Home — KPI overview + revenue trend
"""
import os, sys
APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT    = os.path.dirname(APP_DIR)
sys.path.insert(0, APP_DIR)

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from data_engine import get_kpis, get_monthly

st.set_page_config(
    page_title="TrendPulse Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.main { background-color: #0a0a14; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0f1f 0%, #1a0a2e 100%);
    border-right: 1px solid #2d2d4e;
}
[data-testid="stSidebar"] * { color: #c8c8e8 !important; }

.kpi-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #2d2d5e;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    transition: transform 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); }
.kpi-value { font-size: 1.9rem; font-weight: 700; color: #e94560; margin: 4px 0; }
.kpi-label { font-size: 0.78rem; color: #8888aa; text-transform: uppercase; letter-spacing: 0.08em; }
.kpi-delta { font-size: 0.82rem; color: #00d4aa; margin-top: 4px; }

.section-header {
    font-size: 1.15rem; font-weight: 600; color: #e0e0ff;
    border-left: 3px solid #e94560;
    padding-left: 12px; margin: 28px 0 16px 0;
}
.insight-box {
    background: #12122a;
    border: 1px solid #2a2a4a;
    border-left: 3px solid #f5a623;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 8px 0;
    font-size: 0.88rem;
    color: #c8c8e0;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛍️ TrendPulse")
    st.markdown("*E-Commerce Analytics Platform*")
    st.markdown("---")
    st.markdown("**📋 Navigation**")
    st.markdown("""
    - 🏠 **Home** — Overview
    - 📊 Category Intelligence
    - 🎯 RFM Segmentation
    - 💎 Customer Lifetime Value
    - 🔁 Cohort Retention
    - 🌍 Geographic & Demographics
    - 🔮 Sales Forecast
    """)
    st.markdown("---")
    st.markdown("**📦 Dataset**")
    st.caption("50,000 transactions · 2023–2025")
    st.caption("8 categories · 10 countries")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 8px 0 24px 0">
    <div style="font-size:2rem; font-weight:700; color:#ffffff">
        🛍️ TrendPulse Analytics
    </div>
    <div style="font-size:0.95rem; color:#8888aa; margin-top:4px">
        End-to-end E-Commerce Intelligence Platform &nbsp;·&nbsp;
        Data Analyst Portfolio &nbsp;·&nbsp; Ayush Pandey
    </div>
</div>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
with st.spinner("Running live analysis..."):
    kpis    = get_kpis()
    monthly = get_monthly()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Key Performance Indicators</div>',
            unsafe_allow_html=True)

c1, c2, c3, c4, c5, c6 = st.columns(6)
cards = [
    (c1, "Total Revenue",      f"${kpis['total_revenue']/1e6:.2f}M",  "FY 2023–2025"),
    (c2, "Total Orders",       f"{kpis['total_orders']:,}",            "All time"),
    (c3, "Unique Customers",   f"{kpis['unique_customers']:,}",        "Active base"),
    (c4, "Avg Order Value",    f"${kpis['aov']:.2f}",                 "Per transaction"),
    (c5, "Orders / Customer",  f"{kpis['avg_orders_cust']:.0f}",      "Lifetime avg"),
    (c6, "YoY Growth",         f"{kpis['yoy_growth']:+.1f}%",         "2023 → 2024"),
]
for col, label, value, sub in cards:
    with col:
        color = "#00d4aa" if "+" in value else "#e94560"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value" style="color:{color}">{value}</div>
            <div class="kpi-delta">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Revenue Trend ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Revenue Trend</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📈 Monthly Revenue", "📊 MoM Growth %"])

with tab1:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=monthly["order_month_str"], y=monthly["revenue"],
        name="Monthly Revenue", marker_color="#0f3460",
        opacity=0.85,
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=monthly["order_month_str"], y=monthly["rolling_3m"],
        name="3M Rolling Avg", line=dict(color="#e94560", width=2.5),
        mode="lines+markers", marker=dict(size=5),
        hovertemplate="<b>%{x}</b><br>3M Avg: $%{y:,.0f}<extra></extra>"
    ))
    fig.update_layout(
        template="plotly_dark", height=380,
        paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
        legend=dict(orientation="h", y=1.05),
        xaxis=dict(tickangle=-35, tickfont=dict(size=10)),
        yaxis=dict(tickprefix="$", tickformat=",.0f"),
        margin=dict(l=0, r=0, t=30, b=0),
        hovermode="x unified"
    )
    st.plotly_chart(fig, width="stretch")

with tab2:
    colors = ["#e94560" if v < 0 else "#00d4aa"
              for v in monthly["mom_growth"].fillna(0)]
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=monthly["order_month_str"].iloc[1:],
        y=monthly["mom_growth"].dropna(),
        marker_color=colors[1:],
        hovertemplate="<b>%{x}</b><br>MoM Growth: %{y:.1f}%<extra></extra>"
    ))
    fig2.add_hline(y=0, line_dash="dash", line_color="white", line_width=0.8)
    fig2.update_layout(
        template="plotly_dark", height=380,
        paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
        xaxis=dict(tickangle=-35, tickfont=dict(size=10)),
        yaxis=dict(ticksuffix="%"),
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig2, width="stretch")

# ── Key Insights ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="insight-box">
        💰 <strong>Total revenue of ${kpis['total_revenue']/1e6:.2f}M</strong> across 50,000 transactions
        with a healthy average order value of <strong>${kpis['aov']:.2f}</strong>.
    </div>
    <div class="insight-box">
        📈 <strong>YoY growth of {kpis['yoy_growth']:.1f}%</strong> from 2023 to 2024 —
        confirms strong and consistent business momentum.
    </div>""", unsafe_allow_html=True)
with col2:
    best_month = monthly.loc[monthly["revenue"].idxmax(), "order_month_str"]
    best_rev   = monthly["revenue"].max()
    st.markdown(f"""
    <div class="insight-box">
        🏆 <strong>Best month: {best_month}</strong> with ${best_rev:,.0f} revenue.
        Q4 shows consistent seasonal uplift — plan inventory accordingly.
    </div>
    <div class="insight-box">
        👥 <strong>{kpis['unique_customers']:,} unique customers</strong> averaging
        <strong>{kpis['avg_orders_cust']:.0f} orders each</strong> —
        extremely high repeat purchase rate.
    </div>""", unsafe_allow_html=True)
