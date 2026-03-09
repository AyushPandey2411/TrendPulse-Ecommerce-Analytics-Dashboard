"""pages/5_Geographic_Demographics.py"""
import os, sys
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APP_DIR)

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from data_engine import get_geo

st.set_page_config(page_title="Geographic & Demographics", page_icon="🌍", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0f0f1f,#1a0a2e);border-right:1px solid #2d2d4e;}
[data-testid="stSidebar"] *{color:#c8c8e8 !important;}
.section-header{font-size:1.1rem;font-weight:600;color:#e0e0ff;border-left:3px solid #e94560;padding-left:12px;margin:24px 0 14px 0;}
.insight-box{background:#12122a;border:1px solid #2a2a4a;border-left:3px solid #f5a623;border-radius:8px;padding:12px 16px;margin:6px 0;font-size:0.86rem;color:#c8c8e0;}
</style>""", unsafe_allow_html=True)

st.markdown("## 🌍 Geographic & Demographic Analysis")
st.caption("Country-level performance, age group spending patterns, and payment behaviour.")

with st.spinner("Loading geographic data..."):
    country_stats, age_stats, payment_stats, dow_stats = get_geo()

PALETTE = ["#e94560","#0f3460","#533483","#16213e","#f5a623",
           "#00b4d8","#90e0ef","#caf0f8","#c0392b","#27ae60"]

# ── Country ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Country Performance</div>',
            unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    fig = go.Figure(go.Bar(
        x=country_stats["country"], y=country_stats["revenue"],
        marker=dict(color=PALETTE[:len(country_stats)]),
        text=[f"${v/1000:.0f}K" for v in country_stats["revenue"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<br>Share: " +
                      country_stats["revenue_pct"].apply(lambda x: f"{x:.1f}%").values[0] +
                      "<extra></extra>"
    ))
    fig.update_layout(
        title="Revenue by Country", template="plotly_dark", height=360,
        paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
        yaxis=dict(tickprefix="$", tickformat=",.0f"),
        xaxis=dict(tickangle=-20),
        margin=dict(l=0,r=0,t=40,b=0)
    )
    st.plotly_chart(fig, width="stretch")

with c2:
    country_aov = country_stats.sort_values("avg_order", ascending=True)
    fig2 = go.Figure(go.Bar(
        x=country_aov["avg_order"], y=country_aov["country"],
        orientation="h",
        marker_color="#533483",
        text=[f"${v:.0f}" for v in country_aov["avg_order"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>AOV: $%{x:.2f}<extra></extra>"
    ))
    fig2.update_layout(
        title="Avg Order Value by Country", template="plotly_dark", height=360,
        paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
        xaxis=dict(tickprefix="$"),
        margin=dict(l=0,r=0,t=40,b=0)
    )
    st.plotly_chart(fig2, width="stretch")

# ── Age Demographics ──────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Age Group Analysis</div>',
            unsafe_allow_html=True)
c1, c2 = st.columns(2)

age_colors = ["#e94560","#0f3460","#533483","#f5a623","#00b4d8"]

with c1:
    fig3 = go.Figure(go.Bar(
        x=age_stats["age_group"].astype(str), y=age_stats["revenue"],
        marker=dict(color=age_colors),
        text=[f"${v/1000:.0f}K" for v in age_stats["revenue"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>"
    ))
    fig3.update_layout(
        title="Revenue by Age Group", template="plotly_dark", height=340,
        paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
        yaxis=dict(tickprefix="$", tickformat=",.0f"),
        margin=dict(l=0,r=0,t=40,b=0)
    )
    st.plotly_chart(fig3, width="stretch")

with c2:
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=age_stats["age_group"].astype(str), y=age_stats["avg_order"],
        mode="lines+markers",
        line=dict(color="#e94560", width=2.5),
        marker=dict(size=10, color=age_colors),
        fill="tozeroy", fillcolor="rgba(233,69,96,0.12)",
        hovertemplate="<b>%{x}</b><br>AOV: $%{y:.2f}<extra></extra>"
    ))
    fig4.update_layout(
        title="Avg Order Value Across Age Groups", template="plotly_dark", height=340,
        paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
        yaxis=dict(tickprefix="$"),
        margin=dict(l=0,r=0,t=40,b=0)
    )
    st.plotly_chart(fig4, width="stretch")

# ── Payment & Day of Week ──────────────────────────────────────────────────────
st.markdown('<div class="section-header">Payment Methods & Purchase Timing</div>',
            unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    fig5 = go.Figure(go.Pie(
        labels=payment_stats["payment_method"],
        values=payment_stats["txn_pct"],
        hole=0.55,
        marker=dict(colors=PALETTE[:len(payment_stats)],
                    line=dict(color="#0a0a14", width=2)),
        textinfo="label+percent",
        textfont=dict(size=9, color="white"),
        hovertemplate="<b>%{label}</b><br>Share: %{value:.1f}%<extra></extra>"
    ))
    fig5.update_layout(
        title="Payment Method Share", template="plotly_dark", height=320,
        paper_bgcolor="#0a0a14", showlegend=False,
        annotations=[dict(text="Payments", x=0.5, y=0.5,
                          font=dict(size=11, color="white"), showarrow=False)],
        margin=dict(l=0,r=0,t=40,b=0)
    )
    st.plotly_chart(fig5, width="stretch")

with c2:
    pay_aov = payment_stats.sort_values("avg_order", ascending=True)
    fig6 = go.Figure(go.Bar(
        x=pay_aov["avg_order"], y=pay_aov["payment_method"],
        orientation="h",
        marker_color="#e94560", opacity=0.85,
        text=[f"${v:.0f}" for v in pay_aov["avg_order"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>AOV: $%{x:.2f}<extra></extra>"
    ))
    fig6.update_layout(
        title="AOV by Payment Method", template="plotly_dark", height=320,
        paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
        xaxis=dict(tickprefix="$"),
        margin=dict(l=0,r=0,t=40,b=0)
    )
    st.plotly_chart(fig6, width="stretch")

with c3:
    dow_colors = ["#e94560" if d in ["Saturday","Sunday"] else "#0f3460"
                  for d in dow_stats.index]
    fig7 = go.Figure(go.Bar(
        x=list(dow_stats.index),
        y=list(dow_stats["sum"]),
        marker=dict(color=dow_colors),
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>"
    ))
    fig7.update_layout(
        title="Revenue by Day (Red=Weekend)", template="plotly_dark", height=320,
        paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
        yaxis=dict(tickprefix="$", tickformat=",.0f"),
        xaxis=dict(tickangle=-30, tickfont=dict(size=9)),
        margin=dict(l=0,r=0,t=40,b=0)
    )
    st.plotly_chart(fig7, width="stretch")

# ── Key Insights ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Key Insights</div>',
            unsafe_allow_html=True)
top_country = country_stats.iloc[0]
top_age = age_stats.loc[age_stats["revenue"].idxmax(), "age_group"]

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""<div class="insight-box">
    🌍 <strong>{top_country['country']}</strong> leads with ${top_country['revenue']:,.0f}
    but all 10 countries are within 5% of each other — strong global diversification.
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="insight-box">
    👥 <strong>{top_age} age group</strong> drives the highest revenue — not from higher
    AOV but from more frequent purchases. Target with loyalty programmes.
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class="insight-box">
    💳 Payment methods are evenly split (~17% each). Cash on Delivery remains popular —
    offer COD-to-digital incentive to reduce fulfilment cost.
    </div>""", unsafe_allow_html=True)
