select
    s.website_session_id,
    s.session_created_at,
    s.session_created_at::date as date_day,
    c.channel_id,
    s.user_id,
    s.device_type,
    s.is_repeat_session,
    s.is_converted,
    s.order_id,
    coalesce(s.order_revenue_usd, 0) as revenue_usd
from {{ ref('int_session_to_order') }} s
left join {{ ref('dim_channel') }} c
    on s.utm_source = c.utm_source
    and s.utm_campaign = c.utm_campaign
