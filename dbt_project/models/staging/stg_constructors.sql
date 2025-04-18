{{ config(materialized='view') }}

-- Staging f1_constructors : unnest + dé‑duplication
-- Grain : 1 ligne par constructor_id

with exploded as (
  select
    constructor_id_elem                              as constructor_id,
    constructor_name[OFFSET(pos)]                    as constructor_name,
    constructor_nationality[OFFSET(pos)]             as constructor_nationality
  from {{ source('f1', 'f1_constructors') }}
  cross join unnest(constructor_id) as constructor_id_elem with offset pos
),

dedup as (
  select *,
         row_number() over (
           partition by constructor_id
           order by constructor_name
         ) as rn
  from exploded
)

select * except(rn)
from dedup
where rn = 1