#!/usr/bin/env bash
set -euo pipefail

echo "[1/5] Preprocess raw CSV"
python src/preprocess.py

echo "[2/5] Load staging + build marts"
psql "$DATABASE_URL" -f sql/01_create_tables.sql
psql "$DATABASE_URL" -f sql/02_load_staging.sql
psql "$DATABASE_URL" -f sql/03_build_marts.sql

echo "[3/5] Export marts to CSV for modeling/dashboard"
psql "$DATABASE_URL" -c "\copy mart_daily_kpis to 'data/outputs/marts/mart_daily_kpis.csv' csv header"
psql "$DATABASE_URL" -c "\copy mart_category_daily to 'data/outputs/marts/mart_category_daily.csv' csv header"
psql "$DATABASE_URL" -c "\copy mart_state_daily to 'data/outputs/marts/mart_state_daily.csv' csv header"

echo "[4/5] Forecast + anomalies"
python src/forecast_prophet.py
python src/anomaly_flags.py

echo "[5/5] Done"
