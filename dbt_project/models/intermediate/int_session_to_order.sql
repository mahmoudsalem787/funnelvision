select
    s.website_session_id,
    s.created_at as session_created_at,
    s.user_id,
    s.is_repeat_session,
    s.utm_source,
    s.utm_campaign,
    s.device_type,
    o.order_id,
    o.created_at as order_created_at,
    o.items_purchased,
    o.price_usd as order_revenue_usd,
    o.cogs_usd as order_cogs_usd,
    (o.order_id is not null) as is_converted
from {{ ref('stg_website_sessions') }} s
left join {{ ref('stg_orders') }} o
    on s.website_session_id = o.website_session_id
