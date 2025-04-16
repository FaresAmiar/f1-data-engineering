{{ config(materialized='table') }}

with constructors as (
    select
        constructor_id,
        constructor_name,
        constructor_nationality
    from {{ ref('stg_constructors') }}
)

select * from constructors
