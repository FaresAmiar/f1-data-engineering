{{ config(materialized='table') }}

with race_results as (
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
        driver_id,
        constructor_id
    from {{ ref('stg_race_results') }}
),

enriched_results as (
    select
        rr.*,
        d.driver_id as dim_driver_id,
        c.constructor_id as dim_constructor_id
    from race_results rr
    left join {{ ref('dim_drivers') }} d on rr.driver_id = d.driver_id
    left join {{ ref('dim_constructors') }} c on rr.constructor_id = c.constructor_id
)

select * from enriched_results
