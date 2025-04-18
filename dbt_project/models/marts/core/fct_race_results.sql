{{ config(materialized='table') }}

with base as (
  select
    race_id,
    season,
    round,
    race_name,
    race_date,
    circuit_id,
    circuit_name,
    position,
    points,
    driver_id,        -- STRING, conforme à dim_drivers
    constructor_id
  from {{ ref('stg_race_results') }}
),

enriched as (
  select
    b.*,
    d.driver_sk        as dim_driver_sk,
    c.constructor_sk   as dim_constructor_sk
  from base b
  left join {{ ref('dim_drivers') }}      d using (driver_id)
  left join {{ ref('dim_constructors') }} c using (constructor_id)
)

select * from enriched