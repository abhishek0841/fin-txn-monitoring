import pandas as pd

MART_PATH = "data/outputs/marts/mart_daily_kpis.csv"
FCST_PATH = "data/outputs/forecasts/daily_kpis_forecast.csv"
OUT_PATH  = "data/outputs/forecasts/daily_anomalies.csv"

mart = pd.read_csv(MART_PATH, parse_dates=["dt"])
fcst = pd.read_csv(FCST_PATH, parse_dates=["ds"])

def flag(metric):
    actual = mart[["dt", metric]].rename(columns={"dt":"ds", metric:"actual"})
    pred = fcst[fcst["metric"] == metric][["ds","yhat_lower","yhat_upper","yhat"]]
    j = actual.merge(pred, on="ds", how="inner")
    j["is_anomaly"] = (j["actual"] < j["yhat_lower"]) | (j["actual"] > j["yhat_upper"])
    j["metric"] = metric
    return j

out = pd.concat([flag("txn_count"), flag("total_spend")], ignore_index=True)
out.to_csv(OUT_PATH, index=False)
print("Wrote:", OUT_PATH)
