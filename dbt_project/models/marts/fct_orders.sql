select
    o.order_id,
    o.created_at as order_created_at,
    o.created_at::date as date_day,
    o.website_session_id,
    f.channel_id,
    f.device_type,
    o.user_id,
    o.primary_product_id as product_id,
    o.items_purchased,
    o.price_usd as revenue_usd,
    o.cogs_usd,
    o.price_usd - o.cogs_usd as margin_usd
from {{ ref('stg_orders') }} o
left join {{ ref('fct_sessions') }} f
    on o.website_session_id = f.website_session_id
