SELECT
  driverId AS driver_id,
  code,
  forename,
  surname,
  nationality,
  dob AS date_of_birth
FROM {{ source('f1', 'drivers') }}
