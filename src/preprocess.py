import pandas as pd

RAW_PATH = "data/raw/credit_card_transactions.csv"
OUT_PATH = "data/raw/credit_card_transactions.csv"

df = pd.read_csv(RAW_PATH)

# Parse timestamp + date of birth
df["trans_date_trans_time"] = pd.to_datetime(df["trans_date_trans_time"], errors="coerce")
df["dob"] = pd.to_datetime(df["dob"], errors="coerce").dt.date

# Keep only needed cols
keep = [
    "trans_date_trans_time","cc_num","merchant","category","amt","city","state",
    "lat","long","merch_lat","merch_long","city_pop","job","dob","is_fraud"
]
df = df[keep].dropna(subset=["trans_date_trans_time","amt"])

df.to_csv(OUT_PATH, index=False)
print("Wrote:", OUT_PATH, "rows:", len(df))
