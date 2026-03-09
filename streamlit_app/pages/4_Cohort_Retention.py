"""pages/4_Cohort_Retention.py"""
import os, sys
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APP_DIR)

import streamlit as st
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
from data_engine import get_cohort, get_kpis

st.set_page_config(page_title="Cohort Retention", page_icon="🔁", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0f0f1f,#1a0a2e);border-right:1px solid #2d2d4e;}
[data-testid="stSidebar"] *{color:#c8c8e8 !important;}
.section-header{font-size:1.1rem;font-weight:600;color:#e0e0ff;border-left:3px solid #e94560;padding-left:12px;margin:24px 0 14px 0;}
.insight-box{background:#12122a;border:1px solid #2a2a4a;border-left:3px solid #f5a623;border-radius:8px;padding:12px 16px;margin:6px 0;font-size:0.86rem;color:#c8c8e0;}
.kpi-card{background:linear-gradient(135deg,#1a1a2e,#16213e);border:1px solid #2d2d5e;border-radius:12px;padding:18px 20px;text-align:center;}
.kpi-value{font-size:1.7rem;font-weight:700;color:#e94560;}
.kpi-label{font-size:0.75rem;color:#8888aa;text-transform:uppercase;letter-spacing:0.08em;}
</style>""", unsafe_allow_html=True)

st.markdown("## 🔁 Cohort Retention Analysis")
st.caption("What % of customers return each month after their first purchase?")

with st.spinner("Building cohort matrix..."):
    retention = get_cohort()

# ── Controls ──────────────────────────────────────────────────────────────────
c1, c2 = st.columns([2,1])
with c1:
    n_cohorts = st.slider("Number of cohorts to display", 6, min(24, len(retention)), 12)
with c2:
    n_months = st.slider("Months to show", 3, 13, 13)

retention_disp = retention.iloc[-n_cohorts:, :n_months]

# ── KPIs ──────────────────────────────────────────────────────────────────────
m1_avg   = retention_disp[1].mean() if 1 in retention_disp.columns else 0
m3_avg   = retention_disp[3].mean() if 3 in retention_disp.columns else 0
m6_avg   = retention_disp[6].mean() if 6 in retention_disp.columns else 0
m12_avg  = retention_disp[12].mean() if 12 in retention_disp.columns else 0

cols = st.columns(4)
for col, label, value, sub in [
    (cols[0], "Month 1 Retention",  f"{m1_avg:.1f}%",  "After 1st month"),
    (cols[1], "Month 3 Retention",  f"{m3_avg:.1f}%",  "After 3 months"),
    (cols[2], "Month 6 Retention",  f"{m6_avg:.1f}%",  "After 6 months"),
    (cols[3], "Month 12 Retention", f"{m12_avg:.1f}%", "After 12 months"),
]:
    with col:
        color = "#00d4aa" if float(value.strip("%")) > 50 else "#e94560"
        st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="color:{color}">{value}</div>
        <div style="color:#666688;font-size:0.75rem">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Heatmap ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Cohort Retention Heatmap</div>',
            unsafe_allow_html=True)

z     = retention_disp.fillna(0).values.tolist()
xlabs = [f"M+{int(c)}" for c in retention_disp.columns]
ylabs = [str(idx) for idx in retention_disp.index]
annot = [[f"{v:.0f}%" if v > 0 else "" for v in row] for row in z]

fig = ff.create_annotated_heatmap(
    z=z, x=xlabs, y=ylabs,
    annotation_text=annot,
    colorscale="YlOrRd",
    showscale=True,
    zmin=0, zmax=100
)
fig.update_layout(
    template="plotly_dark",
    height=max(300, n_cohorts * 28 + 80),
    paper_bgcolor="#0a0a14",
    plot_bgcolor="#1a1a2e",
    xaxis=dict(side="bottom", tickfont=dict(size=10)),
    yaxis=dict(tickfont=dict(size=9)),
    margin=dict(l=0, r=0, t=20, b=0)
)
fig.update_traces(
    hovertemplate="Cohort: %{y}<br>Month: %{x}<br>Retention: %{z:.1f}%<extra></extra>"
)
st.plotly_chart(fig, width="stretch")

# ── Retention curve ───────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Average Retention Curve</div>',
            unsafe_allow_html=True)

avg_retention = retention_disp.mean()
fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=[f"M+{int(c)}" for c in avg_retention.index],
    y=avg_retention.values,
    mode="lines+markers",
    line=dict(color="#e94560", width=2.5),
    marker=dict(size=8, color="#e94560"),
    fill="tozeroy",
    fillcolor="rgba(233,69,96,0.15)",
    hovertemplate="<b>%{x}</b><br>Avg Retention: %{y:.1f}%<extra></extra>"
))
fig2.add_hline(y=50, line_dash="dash", line_color="#f5a623",
               annotation_text="50% mark", annotation_font_color="#f5a623")
fig2.update_layout(
    template="plotly_dark", height=320,
    paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
    yaxis=dict(ticksuffix="%", range=[0,105]),
    margin=dict(l=0,r=0,t=20,b=0),
    title="Average Retention Rate Across All Cohorts"
)
st.plotly_chart(fig2, width="stretch")

# ── Insights ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Insights & Recommendations</div>',
            unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"""
    <div class="insight-box">
        📌 <strong>Month 1 retention of {m1_avg:.1f}%</strong> is the key early indicator.
        If this drops below 30%, the post-purchase experience needs improvement.
    </div>
    <div class="insight-box">
        🎯 Cohorts with strongest long-term retention reveal which acquisition channels
        bring the highest-quality customers — use this to reallocate ad spend.
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="insight-box">
        💡 <strong>Month 3 retention of {m3_avg:.1f}%</strong> indicates habitual buyers.
        Target customers approaching month 3 with loyalty incentives before they churn.
    </div>
    <div class="insight-box">
        🔁 High 6-month retention ({m6_avg:.1f}%) means customers are building
        a repeat-purchase habit — strong signal for subscription/loyalty product launch.
    </div>""", unsafe_allow_html=True)
