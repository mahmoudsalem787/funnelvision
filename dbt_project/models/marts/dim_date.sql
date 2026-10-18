with bounds as (
    select
        min(created_at)::date as start_date,
        max(created_at)::date as end_date
    from {{ ref('stg_website_sessions') }}
),

days as (
    select dateadd(day, seq4(), (select start_date from bounds)) as date_day
    from table(generator(rowcount => 2000))
)

select
    date_day,
    year(date_day) as year,
    month(date_day) as month,
    to_char(date_day, 'YYYY-MM') as year_month,
    dayofweek(date_day) as day_of_week,
    dayname(date_day) as day_name
from days
where date_day <= (select end_date from bounds)
