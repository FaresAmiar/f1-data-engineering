{{ config(materialized='view') }}

-- Staging : aplatit le tableau driver_id et dé‑duplique les pilotes

with exploded as (
  select
    driver_id_elem                             as driver_id,
    first_name[OFFSET(pos)]                    as first_name,
    last_name[OFFSET(pos)]                     as last_name,
    safe_cast(dob[OFFSET(pos)] as date)        as date_of_birth,
    nationality[OFFSET(pos)]                   as nationality
  from {{ source('f1', 'f1_drivers') }}
  cross join unnest(driver_id) as driver_id_elem with offset pos
),

dedup as (
  select *,
         row_number() over (partition by driver_id order by date_of_birth) as rn
  from exploded
)

select * except(rn)
from dedup
where rn = 1
