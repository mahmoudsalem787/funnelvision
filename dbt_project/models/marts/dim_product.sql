select
    product_id,
    product_name,
    created_at as launched_at
from {{ ref('stg_products') }}
