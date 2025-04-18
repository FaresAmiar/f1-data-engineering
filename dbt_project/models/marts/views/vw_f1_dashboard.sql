{{ config(materialized='view') }}

-- Vue consolidée pour Looker Studio (ou tout autre outil BI)

select
  f.race_id,
  f.season,
  f.round,
  f.race_name,
  f.race_date,
  f.circuit_id,
  f.circuit_name,
  f.position,
  f.points,
  f.driver_id,
  concat(d.first_name, ' ', d.last_name) as driver_name,
  d.nationality as driver_nationality,
  f.constructor_id,
  c.constructor_name,
  c.constructor_nationality
from {{ ref('fct_race_results') }} f
left join {{ ref('dim_drivers') }}       d using(driver_id)
left join {{ ref('dim_constructors') }}  c using(constructor_id)
