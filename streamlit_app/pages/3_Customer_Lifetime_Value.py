"""pages/3_Customer_Lifetime_Value.py"""
import os, sys
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APP_DIR)

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from data_engine import get_clv

st.set_page_config(page_title="Customer Lifetime Value", page_icon="💎", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0f0f1f,#1a0a2e);border-right:1px solid #2d2d4e;}
[data-testid="stSidebar"] *{color:#c8c8e8 !important;}
.section-header{font-size:1.1rem;font-weight:600;color:#e0e0ff;border-left:3px solid #e94560;padding-left:12px;margin:24px 0 14px 0;}
.kpi-card{background:linear-gradient(135deg,#1a1a2e,#16213e);border:1px solid #2d2d5e;border-radius:12px;padding:18px 20px;text-align:center;}
.kpi-value{font-size:1.7rem;font-weight:700;color:#e94560;margin:4px 0;}
.kpi-label{font-size:0.75rem;color:#8888aa;text-transform:uppercase;letter-spacing:0.08em;}
.insight-box{background:#12122a;border:1px solid #2a2a4a;border-left:3px solid #f5a623;border-radius:8px;padding:12px 16px;margin:6px 0;font-size:0.86rem;color:#c8c8e0;}
</style>""", unsafe_allow_html=True)

st.markdown("## 💎 Customer Lifetime Value")
st.caption("24-month projected CLV — AOV × purchase frequency × 24 months")

with st.spinner("Computing CLV..."):
    cs, tier_summary = get_clv()

# ── KPIs ──────────────────────────────────────────────────────────────────────
c1,c2,c3,c4 = st.columns(4)
for col, label, value in [
    (c1, "Total Projected CLV (24M)", f"${cs['clv_24m'].sum()/1e6:.2f}M"),
    (c2, "Median CLV",                f"${cs['clv_24m'].median():,.0f}"),
    (c3, "Mean CLV",                  f"${cs['clv_24m'].mean():,.0f}"),
    (c4, "Premium Tier Customers",    f"{len(cs[cs['clv_tier']=='Premium']):,}"),
]:
    with col:
        st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">CLV Distribution & Tier Revenue</div>',
            unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=cs["clv_24m"], nbinsx=30,
        marker_color="#e94560", opacity=0.8, name="CLV",
        hovertemplate="CLV Range: $%{x:,.0f}<br>Count: %{y}<extra></extra>"
    ))
    fig.add_vline(x=cs["clv_24m"].median(), line_dash="dash",
                  line_color="#f5a623", line_width=1.5,
                  annotation_text=f"Median ${cs['clv_24m'].median():,.0f}",
                  annotation_font_color="#f5a623")
    fig.add_vline(x=cs["clv_24m"].mean(), line_dash="dash",
                  line_color="#00b4d8", line_width=1.5,
                  annotation_text=f"Mean ${cs['clv_24m'].mean():,.0f}",
                  annotation_font_color="#00b4d8")
    fig.update_layout(
        title="CLV Distribution (24M Projection)", template="plotly_dark", height=370,
        paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
        xaxis=dict(tickprefix="$", tickformat=",.0f"),
        margin=dict(l=0,r=0,t=40,b=0)
    )
    st.plotly_chart(fig, width="stretch")

with c2:
    tier_colors = ["#16213e","#0f3460","#533483","#e94560"]
    fig2 = go.Figure(go.Bar(
        x=tier_summary["clv_tier"].astype(str),
        y=tier_summary["total_projected_rev"],
        marker=dict(color=tier_colors),
        text=[f"${v/1e6:.1f}M" for v in tier_summary["total_projected_rev"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Projected Revenue: $%{y:,.0f}<extra></extra>"
    ))
    fig2.update_layout(
        title="Total Projected Revenue by CLV Tier", template="plotly_dark", height=370,
        paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
        yaxis=dict(tickprefix="$", tickformat=",.0f"),
        margin=dict(l=0,r=0,t=40,b=0)
    )
    st.plotly_chart(fig2, width="stretch")

# ── Scatter: CLV vs orders ────────────────────────────────────────────────────
st.markdown('<div class="section-header">CLV vs Purchase Frequency</div>',
            unsafe_allow_html=True)

fig3 = px.scatter(
    cs, x="orders", y="clv_24m", color="clv_tier",
    size="total_spend",
    color_discrete_map={
        "Low Value":"#16213e","Medium Value":"#0f3460",
        "High Value":"#533483","Premium":"#e94560"
    },
    labels={"orders":"Total Orders","clv_24m":"Projected CLV (24M)"},
    hover_data={"user_name":True,"total_spend":True},
    title="CLV vs Total Orders (size = total spend)"
)
fig3.update_layout(
    template="plotly_dark", height=400,
    paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
    yaxis=dict(tickprefix="$", tickformat=",.0f"),
    margin=dict(l=0,r=0,t=40,b=0)
)
st.plotly_chart(fig3, width="stretch")

# ── Recommendations ───────────────────────────────────────────────────────────
st.markdown('<div class="section-header">CLV-Based Strategy</div>',
            unsafe_allow_html=True)
c1, c2 = st.columns(2)
recs = [
    ("💎 Premium Tier", f"{len(cs[cs['clv_tier']=='Premium'])} customers",
     "Concierge support · VIP events · Priority shipping · Exclusive previews"),
    ("📈 High Value Tier", f"{len(cs[cs['clv_tier']=='High Value'])} customers",
     "Loyalty points acceleration · Category-specific promotions"),
    ("🔄 Medium Value Tier", f"{len(cs[cs['clv_tier']=='Medium Value'])} customers",
     "Bundle offers · Cross-category discovery to increase basket size"),
    ("⬆️ Low Value Tier", f"{len(cs[cs['clv_tier']=='Low Value'])} customers",
     "First-party data collection · Personalised nudges · Re-engagement offers"),
]
for i, (title, badge, action) in enumerate(recs):
    with (c1 if i % 2 == 0 else c2):
        st.markdown(f"""
        <div class="insight-box">
            <strong>{title}</strong>
            <span style="background:#e9456033;color:#e94560;padding:2px 8px;border-radius:4px;
                  font-size:0.75rem;margin-left:8px">{badge}</span>
            <div style="margin-top:6px">→ {action}</div>
        </div>""", unsafe_allow_html=True)

with st.expander("📋 Full Customer CLV Table"):
    disp = cs[["user_name","total_spend","orders","avg_order_value",
               "purchase_freq","clv_24m","clv_tier"]].copy()
    disp["total_spend"]     = disp["total_spend"].apply(lambda x: f"${x:,.0f}")
    disp["avg_order_value"] = disp["avg_order_value"].apply(lambda x: f"${x:.2f}")
    disp["clv_24m"]         = disp["clv_24m"].apply(lambda x: f"${x:,.0f}")
    disp["purchase_freq"]   = disp["purchase_freq"].apply(lambda x: f"{x:.2f}/mo")
    st.dataframe(disp.sort_values("clv_24m", ascending=False),
                 width="stretch", hide_index=True)
