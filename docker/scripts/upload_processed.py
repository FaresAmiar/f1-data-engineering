# upload_processed.py

import os
from google.cloud.storage import Client as StorageClient
from google.cloud.bigquery import Client as BigQueryClient, ExternalConfig, Table

BUCKET_NAME = os.getenv("TF_VAR_bucket_name")
DATASET_ID  = os.getenv("TF_VAR_bq_dataset_name")
LOCAL_ROOT  = "data/processed"
DEST_PREFIX = "processed"

if not BUCKET_NAME or not DATASET_ID:
    raise ValueError("Définir TF_VAR_bucket_name et TF_VAR_bq_dataset_name dans l'environnement.")

def upload_json_files(bucket_name, local_root, dest_prefix):
    storage_client = StorageClient()
    bucket = storage_client.bucket(bucket_name)

    for root, _, files in os.walk(local_root):
        for fname in files:
            if not fname.endswith(".json"):
                continue
            local_path = os.path.join(root, fname)
            rel_path   = os.path.relpath(local_path, local_root)
            blob_name  = f"{dest_prefix}/{rel_path}"
            bucket.blob(blob_name).upload_from_filename(local_path)
            print(f"✅ {local_path} → gs://{bucket_name}/{blob_name}")

def create_external_table(bq_client, dataset_id, table_id, source_uris):
    dataset_ref = bq_client.dataset(dataset_id)
    table_ref   = dataset_ref.table(table_id)

    ext_conf = ExternalConfig("NEWLINE_DELIMITED_JSON")
    ext_conf.autodetect   = True
    ext_conf.source_uris  = source_uris

    table = Table(table_ref)
    table.external_data_configuration = ext_conf

    # Si la table existe déjà, on la supprime
    try:
        bq_client.get_table(table_ref)
        bq_client.delete_table(table_ref)
        print(f"ℹ️ Table `{table_id}` supprimée.")
    except Exception:
        pass

    bq_client.create_table(table)
    print(f"✅ Table `{table_id}` créée dans {dataset_id}.")

if __name__ == "__main__":
    upload_json_files(BUCKET_NAME, LOCAL_ROOT, DEST_PREFIX)
    bq = BigQueryClient(project=os.getenv("TF_VAR_project_id"))

    for subdir in os.listdir(LOCAL_ROOT):
        path = os.path.join(LOCAL_ROOT, subdir)
        if os.path.isdir(path):
            uri_glob = f"gs://{BUCKET_NAME}/{DEST_PREFIX}/{subdir}/*.json"
            create_external_table(bq, DATASET_ID, subdir, [uri_glob])
