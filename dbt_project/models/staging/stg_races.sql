{{ config(materialized='view') }}

-- Staging f1_races : typage + clé technique + dé‑duplication (une ligne par course)

with races as (
  select
    cast(season as int64)  as season,
    cast(round  as int64)  as round,
    race_name,
    cast(race_date as date) as race_date,
    circuit_id,
    circuit_name,
    concat(cast(season as string), '_', cast(round as string)) as race_id
  from {{ source('f1', 'f1_races') }}
),

dedup as (
  select *,
         row_number() over (
           partition by race_id
           order by race_date desc, circuit_name
         ) as rn
  from races
)

select * except(rn)
from dedup
where rn = 1