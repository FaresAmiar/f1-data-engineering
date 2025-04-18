from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, concat_ws, lit, to_date

spark = SparkSession.builder.appName("F1DataProcessing").getOrCreate()
raw = spark.read.option("multiline", "true").json("data/raw/*.json")

# ------ 1) Table des courses (GP) ------
races = (raw
    .select("season", "round",
            col("raceName").alias("race_name"),
            to_date("date").alias("race_date"),
            col("Circuit.circuitId").alias("circuit_id"),
            col("Circuit.circuitName").alias("circuit_name"))
    # clé technique facultative
    .withColumn("race_id", concat_ws("_", col("season"), col("round")))
)
races.write.mode("overwrite").json("data/processed/f1_races")

# ------ 2) Table des résultats (fact) ------
results = (raw
    .withColumn("race_id", concat_ws("_", col("season"), col("round")))
    .withColumn("result", explode("Results"))
    .select(
        "race_id", "season", "round",
        col("result.position").cast("int").alias("position"),
        col("result.points").cast("double").alias("points"),
        col("result.Driver.driverId").alias("driver_id"),
        col("result.Constructor.constructorId").alias("constructor_id")
    )
)
results.write.mode("overwrite").json("data/processed/f1_results")

# ------ 3) Dimensions pilotes & constructeurs ------
drivers = (results
    .select("driver_id",
            col("result.Driver.givenName").alias("first_name"),
            col("result.Driver.familyName").alias("last_name"),
            col("result.Driver.dateOfBirth").alias("dob"),
            col("result.Driver.nationality").alias("nationality"))
    .dropDuplicates()
)
drivers.write.mode("overwrite").json("data/processed/f1_drivers")

constructors = (results
    .select("constructor_id",
            col("result.Constructor.name").alias("constructor_name"),
            col("result.Constructor.nationality").alias("constructor_nationality"))
    .dropDuplicates()
)
constructors.write.mode("overwrite").json("data/processed/f1_constructors")
