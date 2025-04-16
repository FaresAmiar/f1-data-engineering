SELECT
  cast(race_id as int64) as race_id,
  cast(season as int64) as season,
  cast(round as int64) as round,
  race_name,
  cast(race_date as date) as race_date,
  circuit_id,
  circuit_name,
  constructor_id,
  constructor_name,
  constructor_nationality
FROM {{ source('f1', 'race_results') }}
