{{ config(materialized='table') }}

select
  driver_id,                      -- resté en STRING
  first_name,
  last_name,
  date_of_birth,
  nationality,
  row_number() over (order by driver_id) as driver_sk
from {{ ref('stg_drivers') }}