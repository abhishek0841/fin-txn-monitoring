CREATE TABLE IF NOT EXISTS stg_transactions (
  trans_ts           TIMESTAMP,
  cc_num             BIGINT,
  merchant           TEXT,
  category           TEXT,
  amt                NUMERIC(12,2),
  city               TEXT,
  state              TEXT,
  lat                NUMERIC(10,6),
  long               NUMERIC(10,6),
  merch_lat          NUMERIC(10,6),
  merch_long         NUMERIC(10,6),
  city_pop           BIGINT,
  job                TEXT,
  dob                DATE,
  is_fraud           INT
);

CREATE TABLE IF NOT EXISTS mart_daily_kpis (
  dt                DATE PRIMARY KEY,
  txn_count         BIGINT,
  total_spend       NUMERIC(18,2),
  avg_ticket        NUMERIC(12,2),
  unique_cards      BIGINT,
  unique_merchants  BIGINT,
  fraud_rate        NUMERIC(6,4)
);

CREATE TABLE IF NOT EXISTS mart_category_daily (
  dt           DATE,
  category     TEXT,
  txn_count    BIGINT,
  total_spend  NUMERIC(18,2),
  fraud_rate   NUMERIC(6,4),
  PRIMARY KEY (dt, category)
);

CREATE TABLE IF NOT EXISTS mart_state_daily (
  dt           DATE,
  state        TEXT,
  txn_count    BIGINT,
  total_spend  NUMERIC(18,2),
  fraud_rate   NUMERIC(6,4),
  PRIMARY KEY (dt, state)
);
