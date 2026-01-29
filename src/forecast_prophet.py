import pandas as pd
from prophet import Prophet

IN_PATH = "data/outputs/marts/mart_daily_kpis.csv"
OUT_PATH = "data/outputs/forecasts/daily_kpis_forecast.csv"

df = pd.read_csv(IN_PATH)
df["dt"] = pd.to_datetime(df["dt"])

def run_prophet(series_col: str):
    tmp = df[["dt", series_col]].rename(columns={"dt": "ds", series_col: "y"}).dropna()
    m = Prophet(weekly_seasonality=True, yearly_seasonality=True, daily_seasonality=False, interval_width=0.95,changepoint_prior_scale=0.05)
    m.fit(tmp)
    future = m.make_future_dataframe(periods=30)
    fcst = m.predict(future)[["ds","yhat","yhat_lower","yhat_upper"]]
    fcst["metric"] = series_col
    return fcst

fc1 = run_prophet("txn_count")
fc2 = run_prophet("total_spend")

out = pd.concat([fc1, fc2], ignore_index=True)
out.to_csv(OUT_PATH, index=False)
print("Wrote:", OUT_PATH)
