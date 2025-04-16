from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col
import os

def main():
    spark = SparkSession.builder.appName("F1DataProcessing").getOrCreate()

    # Lire tous les fichiers JSON bruts en mode multiline
    input_path = "data/raw/"
    print(os.listdir('/app/data'))
    df = spark.read.option("multiline", "true").json(input_path)

    # Vérifier le schéma pour confirmer la présence d'une colonne de type tableau

    # Supposons que la colonne contenant la liste des courses s'appelle "races"

    # Extraction de la table des courses
    races = df.select(
        col("season").alias("season"),
        col("round").alias("round"),
        col("raceName").alias("race_name"),
        col("date").alias("race_date"),
        col("Circuit.circuitId").alias("circuit_id"),
        col("Circuit.circuitName").alias("circuit_name")
    )
    races.write.mode("overwrite").json("data/processed/f1_races")

    # Extraction de la table des pilotes à partir de Results
    drivers = df.select(
        col("Results.Driver.driverId").alias("driver_id"),
        col("Results.Driver.givenName").alias("first_name"),
        col("Results.Driver.familyName").alias("last_name"),
        col("Results.Driver.dateOfBirth").alias("dob"),
        col("Results.Driver.nationality").alias("nationality")
    ).dropDuplicates()
    drivers.write.mode("overwrite").json("data/processed/f1_drivers")

    # Extraction de la table des constructeurs
    constructors = df.select(
        col("Results.Constructor.constructorId").alias("constructor_id"),
        col("Results.Constructor.name").alias("constructor_name"),
        col("Results.Constructor.nationality").alias("constructor_nationality")
    ).dropDuplicates()
    constructors.write.mode("overwrite").json("data/processed/f1_constructors")

    spark.stop()
    print("Job Spark terminé, données traitées écrites dans data/processed/")

if __name__ == "__main__":
    main()
