select
    order_id,
    created_at::timestamp as created_at,
    website_session_id,
    user_id,
    primary_product_id,
    items_purchased,
    price_usd,
    cogs_usd
from {{ source('raw', 'orders') }}
