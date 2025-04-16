from google.cloud import bigquery
import os

PROJECT_ID = os.getenv("TF_VAR_project_id")  # ex: "mon-projet-gcp"
DATASET_ID = os.getenv("TF_VAR_dataset")    # ex: "f1_raw"
BUCKET = os.getenv("TF_VAR_bucket_name")

client = bigquery.Client()

tables = {
    "race_results": "processed/f1_cleaned/race_results/*.json",
    "drivers": "processed/f1_cleaned/drivers/*.json",
    "constructors": "processed/f1_cleaned/constructors/*.json"
}

for table_id, gcs_path in tables.items():
    table_ref = f"{BUCKET}/{PROJECT_ID}.{DATASET_ID}.{table_id}"
    external_config = bigquery.ExternalConfig("NEWLINE_DELIMITED_JSON")
    external_config.source_uris = [f"gs://{gcs_path}"]
    external_config.autodetect = True

    table = bigquery.Table(table_ref)
    table.external_data_configuration = external_config

    table = client.create_table(table, exists_ok=True)
    print(f"✅ External table created or updated: {table_ref}")
