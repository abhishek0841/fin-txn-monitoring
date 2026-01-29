import pandas as pd
import duckdb
from pathlib import Path

RAW_CLEAN = "data/raw/credit_card_transactions_clean.csv"
OUT_DIR = Path("data/outputs/marts")
OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW_CLEAN, encoding="latin-1")
df["trans_date_trans_time"] = pd.to_datetime(df["trans_date_trans_time"], errors="coerce")
df = df.dropna(subset=["trans_date_trans_time", "amt"])
df["dt"] = df["trans_date_trans_time"].dt.date

con = duckdb.connect("data/outputs/finance.duckdb")
con.register("txns", df)

con.execute("""
CREATE OR REPLACE TABLE mart_daily_kpis AS
SELECT
  dt,
  COUNT(*) AS txn_count,
  SUM(amt) AS total_spend,
  AVG(amt) AS avg_ticket,
  COUNT(DISTINCT cc_num) AS unique_cards,
  COUNT(DISTINCT merchant) AS unique_merchants,
  AVG(is_fraud) AS fraud_rate
FROM txns
GROUP BY dt
ORDER BY dt;
""")

con.execute("COPY mart_daily_kpis TO 'data/outputs/marts/mart_daily_kpis.csv' (HEADER, DELIMITER ',');")
print("✅ Built mart_daily_kpis:", "data/outputs/marts/mart_daily_kpis.csv")
