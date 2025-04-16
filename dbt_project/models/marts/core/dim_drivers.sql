{{ config(materialized='table') }}

with drivers as (
    select
        driver_id,
        code,
        forename,
        surname,
        nationality,
        date_of_birth
    from {{ ref('stg_drivers') }}
)

select * from drivers
