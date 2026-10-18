select
    website_pageview_id,
    created_at::timestamp as created_at,
    website_session_id,
    pageview_url
from {{ source('raw', 'website_pageviews') }}
