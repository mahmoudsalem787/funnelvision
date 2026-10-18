select
    website_session_id,
    created_at::timestamp as created_at,
    user_id,
    is_repeat_session::int = 1 as is_repeat_session,
    coalesce(utm_source, 'direct') as utm_source,
    coalesce(utm_campaign, 'none') as utm_campaign,
    utm_content,
    device_type,
    http_referer
from {{ source('raw', 'website_sessions') }}
