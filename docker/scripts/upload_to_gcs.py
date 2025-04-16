from google.cloud import storage
import os

# Paramètres
BUCKET_NAME = os.getenv("TF_VAR_bucket_name")
LOCAL_FOLDER = "data/raw"  # Dossier où sont stockés les fichiers JSON

if not BUCKET_NAME:
    raise ValueError("La variable d'environnement TF_VAR_bucket_name est manquante.")


def upload_to_gcs(bucket_name, local_folder):
    """Upload tous les fichiers JSON de local_folder vers GCS"""
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    for filename in os.listdir(local_folder):
        if filename.endswith(".json"):
            blob = bucket.blob(f"raw/{filename}")  # Stockage sous 'raw/'
            blob.upload_from_filename(os.path.join(local_folder, filename))
            print(f"✅ {filename} uploadé sur GCS")

if __name__ == "__main__":
    upload_to_gcs(BUCKET_NAME, LOCAL_FOLDER)
