"""pages/7_Sales_Forecast.py"""
import os, sys
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APP_DIR)

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from data_engine import get_monthly

st.set_page_config(page_title="Sales Forecast", page_icon="🔮", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0f0f1f,#1a0a2e);border-right:1px solid #2d2d4e;}
[data-testid="stSidebar"] *{color:#c8c8e8 !important;}
.section-header{font-size:1.1rem;font-weight:600;color:#e0e0ff;border-left:3px solid #e94560;padding-left:12px;margin:24px 0 14px 0;}
.kpi-card{background:linear-gradient(135deg,#1a1a2e,#16213e);border:1px solid #2d2d5e;border-radius:12px;padding:18px 20px;text-align:center;}
.kpi-value{font-size:1.7rem;font-weight:700;color:#e94560;}
.kpi-label{font-size:0.75rem;color:#8888aa;text-transform:uppercase;letter-spacing:0.08em;}
.insight-box{background:#12122a;border:1px solid #2a2a4a;border-left:3px solid #f5a623;border-radius:8px;padding:12px 16px;margin:6px 0;font-size:0.86rem;color:#c8c8e0;}
</style>""", unsafe_allow_html=True)

st.markdown("## 🔮 Sales Forecast")
st.caption("Meta Prophet time-series model — yearly seasonality · 90% confidence interval")

with st.spinner("Loading monthly data..."):
    monthly = get_monthly()

# ── Controls ──────────────────────────────────────────────────────────────────
c1, c2 = st.columns([2,1])
with c2:
    forecast_months = st.selectbox("Forecast horizon", [3, 6, 9, 12], index=1)

# ── Train Prophet ─────────────────────────────────────────────────────────────
with st.spinner(f"Training Prophet model and forecasting {forecast_months} months..."):
    try:
        from prophet import Prophet
        prophet_df = (monthly
                      .rename(columns={"order_month_str":"ds","revenue":"y"})[["ds","y"]]
                      .copy())
        prophet_df["ds"] = pd.to_datetime(prophet_df["ds"])

        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            changepoint_prior_scale=0.05,
            seasonality_prior_scale=10,
            interval_width=0.90
        )
        model.fit(prophet_df)
        future   = model.make_future_dataframe(periods=forecast_months, freq="MS")
        forecast = model.predict(future)
        prophet_ok = True
    except Exception as e:
        st.error(f"Prophet error: {e}")
        prophet_ok = False

if prophet_ok:
    future_only   = forecast[forecast["ds"] > prophet_df["ds"].max()]
    total_forecast = future_only["yhat"].sum()
    upper_forecast = future_only["yhat_upper"].sum()
    lower_forecast = future_only["yhat_lower"].sum()
    last_actual    = prophet_df["y"].iloc[-1]
    next_forecast  = future_only["yhat"].iloc[0] if len(future_only) > 0 else 0
    growth_pct     = (next_forecast - last_actual) / last_actual * 100

    # ── KPIs ──────────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    for col, label, value, color in [
        (c1, f"Projected {forecast_months}M Revenue",
             f"${total_forecast/1e6:.2f}M", "#e94560"),
        (c2, "Optimistic Scenario (Upper)",
             f"${upper_forecast/1e6:.2f}M", "#00d4aa"),
        (c3, "Conservative Scenario (Lower)",
             f"${lower_forecast/1e6:.2f}M", "#f5a623"),
        (c4, "Next Month Growth vs Actual",
             f"{growth_pct:+.1f}%", "#00d4aa" if growth_pct > 0 else "#e94560"),
    ]:
        with col:
            st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value" style="color:{color}">{value}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Main forecast chart ────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Revenue Forecast</div>',
                unsafe_allow_html=True)

    fig = go.Figure()

    # Confidence band
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast["ds"], forecast["ds"][::-1]]).tolist(),
        y=pd.concat([forecast["yhat_upper"], forecast["yhat_lower"][::-1]]).tolist(),
        fill="toself",
        fillcolor="rgba(233,69,96,0.12)",
        line=dict(color="rgba(0,0,0,0)"),
        name="90% Confidence Interval",
        hoverinfo="skip"
    ))

    # Forecast line
    fig.add_trace(go.Scatter(
        x=forecast["ds"], y=forecast["yhat"],
        name="Forecast", mode="lines",
        line=dict(color="#e94560", width=2, dash="dash"),
        hovertemplate="<b>%{x|%b %Y}</b><br>Forecast: $%{y:,.0f}<extra></extra>"
    ))

    # Actual data
    fig.add_trace(go.Scatter(
        x=prophet_df["ds"], y=prophet_df["y"],
        name="Actual Revenue", mode="lines+markers",
        line=dict(color="#00b4d8", width=2),
        marker=dict(size=6, color="#00b4d8"),
        hovertemplate="<b>%{x|%b %Y}</b><br>Actual: $%{y:,.0f}<extra></extra>"
    ))

    # Divider
    split = prophet_df["ds"].max()
    fig.add_vline(x=split, line_dash="dot", line_color="#f5a623",
                  line_width=1.5)
    fig.add_annotation(x=split, y=1, yref="paper",
                       text="Forecast →", font=dict(color="#f5a623", size=11),
                       showarrow=False, xanchor="left", yanchor="bottom")

    fig.update_layout(
        template="plotly_dark", height=450,
        paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
        legend=dict(orientation="h", y=1.05),
        yaxis=dict(tickprefix="$", tickformat=",.0f"),
        xaxis=dict(tickformat="%b %Y"),
        hovermode="x unified",
        margin=dict(l=0,r=0,t=40,b=0)
    )
    st.plotly_chart(fig, width="stretch")

    # ── Seasonality components ─────────────────────────────────────────────────
    st.markdown('<div class="section-header">Seasonality Component</div>',
                unsafe_allow_html=True)

    seasonal = forecast[["ds","trend","yearly"]].copy()
    seasonal = seasonal[seasonal["ds"].isin(prophet_df["ds"])]

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=seasonal["ds"], y=seasonal["trend"],
        name="Trend", mode="lines",
        line=dict(color="#00b4d8", width=2),
        hovertemplate="<b>%{x|%b %Y}</b><br>Trend: $%{y:,.0f}<extra></extra>"
    ))
    fig2.add_trace(go.Bar(
        x=seasonal["ds"], y=seasonal["yearly"],
        name="Yearly Seasonality",
        marker_color="#533483", opacity=0.7,
        hovertemplate="<b>%{x|%b %Y}</b><br>Seasonal effect: $%{y:,.0f}<extra></extra>"
    ))
    fig2.update_layout(
        template="plotly_dark", height=320,
        paper_bgcolor="#0a0a14", plot_bgcolor="#1a1a2e",
        legend=dict(orientation="h", y=1.05),
        yaxis=dict(tickprefix="$"),
        margin=dict(l=0,r=0,t=30,b=0)
    )
    st.plotly_chart(fig2, width="stretch")

    # ── Forecast table ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Forecast Data Table</div>',
                unsafe_allow_html=True)

    forecast_table = future_only[["ds","yhat","yhat_lower","yhat_upper"]].copy()
    forecast_table.columns = ["Month","Forecast","Lower Bound","Upper Bound"]
    forecast_table["Month"] = forecast_table["Month"].dt.strftime("%b %Y")
    for col in ["Forecast","Lower Bound","Upper Bound"]:
        forecast_table[col] = forecast_table[col].apply(lambda x: f"${x:,.0f}")

    st.dataframe(forecast_table, width="stretch", hide_index=True)

    # ── Planning guide ────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Planning Guide</div>',
                unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="insight-box">
        📦 <strong>Inventory planning:</strong> Use the <em>Upper Bound</em>
        (${upper_forecast/1e6:.2f}M) as your optimistic scenario.
        Stock 15–20% buffer for Electronics & Toys heading into Q4.
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="insight-box">
        💰 <strong>Budget planning:</strong> Use the <em>Lower Bound</em>
        (${lower_forecast/1e6:.2f}M) for conservative cost planning.
        The 90% CI means actual revenue should fall within this range 90% of the time.
        </div>""", unsafe_allow_html=True)
