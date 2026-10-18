import os

import pandas as pd
import plotly.express as px
import snowflake.connector
import streamlit as st

st.set_page_config(page_title="FunnelVision", layout="wide")
st.title("FunnelVision: E-Commerce Marketing Analytics")

MARTS = "FUNNELVISION.ANALYTICS_MARTS"


@st.cache_resource
def get_conn():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        role=os.environ["SNOWFLAKE_ROLE"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
    )


@st.cache_data(ttl=3600)
def run_query(sql: str) -> pd.DataFrame:
    cur = get_conn().cursor()
    try:
        cur.execute(sql)
        df = cur.fetch_pandas_all()
    finally:
        cur.close()
    df.columns = [c.lower() for c in df.columns]
    return df


# ---------- Filters ----------
bounds = run_query(
    f"select min(date_day) as d0, max(date_day) as d1 from {MARTS}.fct_sessions"
)
min_d, max_d = bounds["d0"][0], bounds["d1"][0]

st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Date range", value=(min_d, max_d), min_value=min_d, max_value=max_d
)
devices = st.sidebar.multiselect(
    "Device", ["desktop", "mobile"], default=["desktop", "mobile"]
)

if len(date_range) != 2 or not devices:
    st.info("Pick a start and end date and at least one device.")
    st.stop()

d_from, d_to = date_range
dev_list = ", ".join(f"'{d}'" for d in devices)
where = (
    f"date_day between '{d_from}' and '{d_to}' and device_type in ({dev_list})"
)

# ---------- KPIs ----------
kpi = run_query(
    f"""
    select count(*) as sessions,
           sum(iff(is_converted, 1, 0)) as orders,
           sum(revenue_usd) as revenue
    from {MARTS}.fct_sessions where {where}
    """
).iloc[0]

refund = run_query(
    f"""
    select count(*) as items,
           sum(iff(is_refunded, 1, 0)) as refunded
    from {MARTS}.fct_refunds
    where date_day between '{d_from}' and '{d_to}'
    """
).iloc[0]

sessions = int(kpi["sessions"] or 0)
orders = int(kpi["orders"] or 0)
revenue = float(kpi["revenue"] or 0)
conv = orders / sessions * 100 if sessions else 0
items = int(refund["items"] or 0)
refund_rate = int(refund["refunded"] or 0) / items * 100 if items else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"${revenue:,.0f}")
c2.metric("Orders", f"{orders:,}")
c3.metric("Conversion rate", f"{conv:.2f}%")
c4.metric("Refund rate", f"{refund_rate:.2f}%")

# ---------- Charts ----------
left, right = st.columns(2)

monthly = run_query(
    f"""
    select to_char(date_day, 'YYYY-MM') as month, sum(revenue_usd) as revenue
    from {MARTS}.fct_sessions where {where}
    group by 1 order by 1
    """
)
left.plotly_chart(
    px.line(monthly, x="month", y="revenue", title="Monthly revenue"),
    use_container_width=True,
)

by_channel = run_query(
    f"""
    select c.channel_name, sum(s.revenue_usd) as revenue
    from {MARTS}.fct_sessions s
    join {MARTS}.dim_channel c on s.channel_id = c.channel_id
    where {where.replace('date_day', 's.date_day').replace('device_type', 's.device_type')}
    group by 1 order by 2 desc
    """
)
right.plotly_chart(
    px.bar(by_channel, x="channel_name", y="revenue", title="Revenue by channel"),
    use_container_width=True,
)

by_product = run_query(
    f"""
    select p.product_name,
           avg(iff(r.is_refunded, 1, 0)) * 100 as refund_rate
    from {MARTS}.fct_refunds r
    join {MARTS}.dim_product p on r.product_id = p.product_id
    where r.date_day between '{d_from}' and '{d_to}'
    group by 1 order by 2 desc
    """
)
st.plotly_chart(
    px.bar(by_product, x="product_name", y="refund_rate",
           title="Refund rate by product (%)"),
    use_container_width=True,
)
