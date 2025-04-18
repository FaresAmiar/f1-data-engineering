{{ config(materialized='table') }}

select
  constructor_id,                    -- STRING, conforme au staging
  constructor_name,
  constructor_nationality,
  row_number() over (order by constructor_id) as constructor_sk
from {{ ref('stg_constructors') }}
