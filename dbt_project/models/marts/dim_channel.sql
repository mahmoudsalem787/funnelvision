with channels as (
    select distinct
        utm_source,
        utm_campaign
    from {{ ref('stg_website_sessions') }}
)

select
    row_number() over (order by utm_source, utm_campaign) as channel_id,
    utm_source,
    utm_campaign,
    utm_source || ' / ' || utm_campaign as channel_name
from channels
