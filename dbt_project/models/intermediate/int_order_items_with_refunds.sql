select
    oi.order_item_id,
    oi.order_id,
    oi.product_id,
    oi.created_at,
    oi.is_primary_item,
    oi.price_usd,
    oi.cogs_usd,
    r.order_item_refund_id,
    coalesce(r.refund_amount_usd, 0) as refund_amount_usd,
    (r.order_item_refund_id is not null) as is_refunded
from {{ ref('stg_order_items') }} oi
left join {{ ref('stg_order_item_refunds') }} r
    on oi.order_item_id = r.order_item_id
