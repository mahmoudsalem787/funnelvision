select
    product_id,
    created_at::timestamp as created_at,
    product_name
from {{ source('raw', 'products') }}
