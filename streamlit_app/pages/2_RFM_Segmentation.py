"""
pages/2_RFM_Segmentation.py
"""
import os, sys
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APP_DIR)

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from data_engine import get_rfm

st.set_page_config(page_title="RFM Segmentation", page_icon="🎯", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0f0f1f,#1a0a2e);border-right:1px solid #2d2d4e;}
[data-testid="stSidebar"] *{color:#c8c8e8 !important;}
.section-header{font-size:1.1rem;font-weight:600;color:#e0e0ff;border-left:3px solid #e94560;padding-left:12px;margin:24px 0 14px 0;}
.seg-card{border-radius:10px;padding:14px 18px;margin:6px 0;color:white;font-size:0.85rem;}
.insight-box{background:#12122a;border:1px solid #2a2a4a;border-left:3px solid #f5a623;border-radius:8px;padding:12px 16px;margin:6px 0;font-size:0.86rem;color:#c8c8e0;}
</style>""", unsafe_allow_html=True)

SEG_COLORS = {
    "Champions":          "#e94560",
    "Loyal Customers":    "#0f3460",
    "New Customers":      "#00b4d8",
    "Potential Loyalists":"#533483",
    "Needs Attention":    "#f5a623",
    "At Risk":            "#e07b54",
    "Cannot Lose Them":   "#c0392b",
    "Lost Customers":     "#555577",
    "Hibernating":        "#334455",
}

SEG_ACTIONS = {
    "Champions":           "VIP loyalty tier — early access, exclusive offers, concierge support",
    "Loyal Customers":     "Upsell premium/higher-margin products like Electronics",
    "New Customers":       "3-email onboarding sequence + 2nd-purchase discount",
    "Potential Loyalists": "Personalised recommendations + loyalty points incentive",
    "Needs Attention":     "Re-engagement campaign before they become At Risk",
    "At Risk":             "Personalised win-back email within 7 days of lapse",
    "Cannot Lose Them":    "High-value retention offer — free shipping, personal outreach",
    "Lost Customers":      "15–20% discount win-back campaign (last resort)",
    "Hibernating":         "Reactivation survey to understand drop-off reason",
}

st.markdown("## 🎯 RFM Customer Segmentation")
st.caption("Recency · Frequency · Monetary — quintile-based scoring (industry standard)")

with st.spinner("Computing RFM scores..."):
    rfm, seg_summary = get_rfm()

# ── Segment filter ────────────────────────────────────────────────────────────
all_segs = sorted(seg_summary["segment"].tolist())
selected = st.multiselect("Filter segments", all_segs, default=all_segs,
                           key="seg_filter")
seg_filtered = seg_summary[seg_summary["segment"].isin(selected)]

# ── Row 1 — Segment cards ─────────────────────────────────────────────────────
st.markdown('<div class="section-header">Segment Overview</div>',
            unsafe_allow_html=True)

cols = st.columns(len(seg_filtered) if len(seg_filtered) <= 5 else 5)
for i, (_, row) in enumerate(seg_filtered.iterrows()):
    col = cols[i % 5]
    color = SEG_COLORS.get(row["segment"], "#333355")
    with col:
        st.markdown(f"""
        <div class="seg-card" style="background:linear-gradient(135deg,{color}44,{color}22);
             border:1px solid {color}88;">
            <div style="font-weight:700;font-size:0.95rem;color:{color}">{row['segment']}</div>
            <div style="font-size:1.5rem;font-weight:700;color:white">{int(row['customers'])}</div>
            <div style="color:#aaaacc;font-size:0.75rem">customers</div>
            <div style="color:#f5a623;font-size:0.8rem;margin-top:4px">
                ${row['avg_monetary']:,.0f} avg spend
            </div>
        </div>""", unsafe_allow_html=True)

# ── Row 2 — Charts ────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Segment Analysis</div>',
            unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    # Bubble: Recency vs Frequency, size = revenue
    fig = px.scatter(
        seg_filtered,
        x="avg_recency", y="avg_frequency",
        size="total_revenue", color="segment",
        text="segment",
        color_discrete_map=SEG_COLORS,
        size_max=50,
        labels={"avg_recency":"Avg Recency (days — lower = better)",
                "avg_frequency":"Avg Frequency (orders)"},
        title="Recency vs Frequency (bubble = revenue)"
    )
    fig.update_traces(textposition="top center", textfont=dict(size=9, color="white"))
    fig.update_layout(
        template="plotly_dark", height=380,
        paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
        showlegend=False, margin=dict(l=0,r=0,t=40,b=0)
    )
    st.plotly_chart(fig, width="stretch")

with c2:
    # Revenue donut
    fig2 = go.Figure(go.Pie(
        labels=seg_filtered["segment"],
        values=seg_filtered["revenue_pct"],
        hole=0.55,
        marker=dict(colors=[SEG_COLORS.get(s,"#333355")
                             for s in seg_filtered["segment"]],
                    line=dict(color="#0a0a14", width=2)),
        textinfo="label+percent",
        textfont=dict(size=10, color="white"),
        hovertemplate="<b>%{label}</b><br>Revenue share: %{value:.1f}%<extra></extra>"
    ))
    fig2.update_layout(
        title="Revenue Share by Segment",
        template="plotly_dark", height=380,
        paper_bgcolor="#0a0a14",
        showlegend=False,
        annotations=[dict(text="Revenue<br>Share", x=0.5, y=0.5,
                          font=dict(size=12, color="white"),
                          showarrow=False)],
        margin=dict(l=0,r=0,t=40,b=0)
    )
    st.plotly_chart(fig2, width="stretch")

# ── Avg monetary bar ──────────────────────────────────────────────────────────
seg_mon = seg_filtered.sort_values("avg_monetary", ascending=True)
fig3 = go.Figure(go.Bar(
    x=seg_mon["avg_monetary"], y=seg_mon["segment"],
    orientation="h",
    marker=dict(color=[SEG_COLORS.get(s,"#333355") for s in seg_mon["segment"]]),
    text=[f"${v:,.0f}" for v in seg_mon["avg_monetary"]],
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>Avg Spend: $%{x:,.0f}<extra></extra>"
))
fig3.update_layout(
    title="Average Customer Lifetime Spend by Segment",
    template="plotly_dark", height=320,
    paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
    xaxis=dict(tickprefix="$", tickformat=",.0f"),
    margin=dict(l=0,r=0,t=40,b=0)
)
st.plotly_chart(fig3, width="stretch")

# ── Action Plan ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Marketing Action Plan</div>',
            unsafe_allow_html=True)

cols2 = st.columns(2)
for i, (_, row) in enumerate(seg_filtered.iterrows()):
    col = cols2[i % 2]
    color = SEG_COLORS.get(row["segment"], "#333355")
    action = SEG_ACTIONS.get(row["segment"], "Review and plan engagement strategy")
    with col:
        st.markdown(f"""
        <div style="background:#12122a;border:1px solid #2a2a4a;
             border-left:4px solid {color};border-radius:8px;
             padding:12px 16px;margin:6px 0;">
            <div style="font-weight:600;color:{color};font-size:0.9rem">
                {row['segment']}
                <span style="color:#888;font-size:0.8rem;font-weight:400">
                  · {int(row['customers'])} customers
                </span>
            </div>
            <div style="color:#c8c8e0;font-size:0.83rem;margin-top:6px">
                🎯 {action}
            </div>
        </div>""", unsafe_allow_html=True)

# ── Customer Explorer ─────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Customer Explorer</div>',
            unsafe_allow_html=True)

selected_seg = st.selectbox("View customers in segment",
                             ["All"] + all_segs)
rfm_display = rfm if selected_seg == "All" else rfm[rfm["segment"] == selected_seg]
rfm_show = rfm_display[["user_name","recency","frequency","monetary",
                          "r_score","f_score","m_score","rfm_score","segment"]].copy()
rfm_show["monetary"] = rfm_show["monetary"].apply(lambda x: f"${x:,.0f}")
st.dataframe(rfm_show.sort_values("rfm_score", ascending=False),
             width="stretch", hide_index=True)
