{{ config(materialized='view') }}

-- Staging f1_results : typage, dé‑duplication par (race_id, driver_id)

with results as (
    select
        cast(race_id        as string)  as race_id,        -- ex. "2023_1"
        cast(season         as int64)   as season,
        cast(round          as int64)   as round,
        cast(position       as int64)   as position,
        cast(points         as float64) as points,
        cast(driver_id      as string)  as driver_id,
        cast(constructor_id as string)  as constructor_id
    from {{ source('f1', 'f1_results') }}
),

dedup as (
    select
        *,
        row_number() over (
            partition by race_id, driver_id
            order by position asc, points desc, constructor_id
        ) as rn
    from results
),

clean as (
    select * except(rn)
    from dedup
    where rn = 1
),

races as (
    select
        race_id,
        race_name,
        race_date,
        circuit_id,
        circuit_name
    from {{ ref('stg_races') }}
)

select
    c.season,
    c.round,
    r.race_name,
    r.race_date,
    r.circuit_id,
    r.circuit_name,
    c.position,
    c.points,
    c.driver_id,
    c.constructor_id,
    c.race_id
from clean c
left join races r using (race_id)
