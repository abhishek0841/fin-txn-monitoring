import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

MART_PATH = "data/outputs/marts/mart_daily_kpis.csv"
ANOM_PATH = "data/outputs/forecasts/daily_anomalies.csv"

st.set_page_config(page_title="Transaction Monitoring Dashboard", layout="wide")

st.title("Financial Transaction Monitoring & Forecasting")
st.caption("Daily KPI marts + Prophet forecast bands + anomaly flags (DuckDB + Python).")

# ---------- Load data ----------
@st.cache_data
def load_data():
    mart = pd.read_csv(MART_PATH, parse_dates=["dt"])
    anom = pd.read_csv(ANOM_PATH, parse_dates=["ds"])
    return mart, anom

mart, anom = load_data()

# ---------- Sidebar controls ----------
st.sidebar.header("Controls")
metric = st.sidebar.selectbox("Metric", ["txn_count", "total_spend"])
show_conf_band = st.sidebar.checkbox("Show forecast confidence band", value=True)
show_anoms = st.sidebar.checkbox("Show anomalies", value=True)

date_min = mart["dt"].min()
date_max = mart["dt"].max()
date_range = st.sidebar.date_input("Date range", (date_min.date(), date_max.date()))
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start_date, end_date = date_min, date_max

# Filter
mart_f = mart[(mart["dt"] >= start_date) & (mart["dt"] <= end_date)].copy()
anom_m = anom[anom["metric"] == metric].copy()
anom_f = anom_m[(anom_m["ds"] >= start_date) & (anom_m["ds"] <= end_date)].copy()

# Merge actual + forecast for plotting
plot_df = mart_f[["dt", metric]].rename(columns={"dt": "ds", metric: "actual"}).merge(
    anom_f[["ds", "yhat", "yhat_lower", "yhat_upper", "is_anomaly"]],
    on="ds", how="left"
)

# ---------- KPI tiles ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Days", len(mart_f))
c2.metric("Total txns", f"{int(mart_f['txn_count'].sum()):,}")
c3.metric("Total spend", f"{mart_f['total_spend'].sum():,.0f}")
c4.metric("Avg fraud rate", f"{mart_f['fraud_rate'].mean():.4f}")

st.divider()

# ---------- Main chart ----------
fig = go.Figure()

# Actual line
fig.add_trace(go.Scatter(
    x=plot_df["ds"], y=plot_df["actual"],
    mode="lines", name="Actual"
))

# Forecast line
fig.add_trace(go.Scatter(
    x=plot_df["ds"], y=plot_df["yhat"],
    mode="lines", name="Forecast"
))

# Confidence band
if show_conf_band:
    fig.add_trace(go.Scatter(
        x=pd.concat([plot_df["ds"], plot_df["ds"][::-1]]),
        y=pd.concat([plot_df["yhat_upper"], plot_df["yhat_lower"][::-1]]),
        fill="toself",
        line=dict(width=0),
        name="Confidence band",
        hoverinfo="skip",
        opacity=0.2
    ))

# Anomaly markers
if show_anoms:
    anoms_only = plot_df[plot_df["is_anomaly"] == True]
    fig.add_trace(go.Scatter(
        x=anoms_only["ds"], y=anoms_only["actual"],
        mode="markers", name="Anomaly"
    ))

fig.update_layout(
    height=520,
    xaxis_title="Date",
    yaxis_title=metric,
    legend_title="Series"
)

st.plotly_chart(fig, use_container_width=True)

# ---------- Drill tables ----------
st.subheader("Anomalies Table")
if show_anoms:
    tbl = anom_f[anom_f["is_anomaly"] == True].copy()
    tbl = tbl.sort_values("ds").head(200)
    st.dataframe(tbl, use_container_width=True)
else:
    st.info("Enable 'Show anomalies' to see the anomaly table.")

st.subheader("Daily KPI Mart")
st.dataframe(mart_f.head(50), use_container_width=True)
