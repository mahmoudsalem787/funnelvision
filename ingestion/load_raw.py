import os

import snowflake.connector

DATA_DIR = "/opt/airflow/data"

TABLES = {
    "products": "product_id NUMBER, created_at TIMESTAMP_NTZ, product_name VARCHAR",
    "orders": "order_id NUMBER, created_at TIMESTAMP_NTZ, website_session_id NUMBER, "
              "user_id NUMBER, primary_product_id NUMBER, items_purchased NUMBER, "
              "price_usd NUMBER(10,2), cogs_usd NUMBER(10,2)",
    "order_items": "order_item_id NUMBER, created_at TIMESTAMP_NTZ, order_id NUMBER, "
                   "product_id NUMBER, is_primary_item NUMBER, "
                   "price_usd NUMBER(10,2), cogs_usd NUMBER(10,2)",
    "order_item_refunds": "order_item_refund_id NUMBER, created_at TIMESTAMP_NTZ, "
                          "order_item_id NUMBER, order_id NUMBER, "
                          "refund_amount_usd NUMBER(10,2)",
    "website_sessions": "website_session_id NUMBER, created_at TIMESTAMP_NTZ, user_id NUMBER, "
                        "is_repeat_session NUMBER, utm_source VARCHAR, utm_campaign VARCHAR, "
                        "utm_content VARCHAR, device_type VARCHAR, http_referer VARCHAR",
    "website_pageviews": "website_pageview_id NUMBER, created_at TIMESTAMP_NTZ, "
                         "website_session_id NUMBER, pageview_url VARCHAR",
}

conn = snowflake.connector.connect(
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    user=os.environ["SNOWFLAKE_USER"],
    password=os.environ["SNOWFLAKE_PASSWORD"],
    role=os.environ["SNOWFLAKE_ROLE"],
    warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
    database=os.environ["SNOWFLAKE_DATABASE"],
    schema="RAW",
)
cur = conn.cursor()

cur.execute(
    "CREATE OR REPLACE FILE FORMAT FUNNEL_CSV TYPE = CSV SKIP_HEADER = 1 "
    "FIELD_OPTIONALLY_ENCLOSED_BY = '\"' NULL_IF = ('')"
)
cur.execute("CREATE STAGE IF NOT EXISTS FUNNEL_STAGE")

import sys
selected = sys.argv[1:] or list(TABLES)
for table in selected:
    columns = TABLES[table]
    print(f"Loading {table} ...", flush=True)
    cur.execute(f"CREATE OR REPLACE TABLE {table} ({columns})")
    cur.execute(
        f"PUT file://{DATA_DIR}/{table}.csv @FUNNEL_STAGE "
        "AUTO_COMPRESS=TRUE OVERWRITE=TRUE"
    )
    cur.execute(
        f"COPY INTO {table} FROM @FUNNEL_STAGE/{table}.csv.gz "
        "FILE_FORMAT = (FORMAT_NAME = FUNNEL_CSV) ON_ERROR = ABORT_STATEMENT"
    )
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"  {table}: {cur.fetchone()[0]} rows", flush=True)

cur.close()
conn.close()
print("All tables loaded.")
