SELECT
  constructorId AS constructor_id,
  name AS constructor_name,
  nationality AS constructor_nationality
FROM {{ source('f1', 'constructors') }}
