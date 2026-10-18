select
    order_item_id,
    order_id,
    product_id,
    created_at::date as date_day,
    price_usd,
    is_refunded,
    refund_amount_usd
from {{ ref('int_order_items_with_refunds') }}
