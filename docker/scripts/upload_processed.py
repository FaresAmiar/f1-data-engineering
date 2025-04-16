import os
from google.cloud import storage

# Le nom du bucket est récupéré via la variable d'environnement
BUCKET_NAME = os.getenv("TF_VAR_bucket_name")
LOCAL_ROOT = "data/processed"  # Dossier racine contenant les sous-dossiers (races, drivers, constructors)

if not BUCKET_NAME:
    raise ValueError("La variable d'environnement TF_VAR_bucket_name n'est pas définie.")

def upload_recursively(bucket_name, local_root, destination_prefix):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    # Parcours récursif du dossier racine
    for root, dirs, files in os.walk(local_root):
        for file in files:
            if file.endswith(".json"):
                local_path = os.path.join(root, file)
                # Conserver la structure relative par rapport au dossier local
                relative_path = os.path.relpath(local_path, local_root)
                destination_blob_name = f"{destination_prefix}/{relative_path}"
                blob = bucket.blob(destination_blob_name)
                blob.upload_from_filename(local_path)
                print(f"✅ {local_path} uploadé vers gs://{bucket_name}/{destination_blob_name}")

if __name__ == "__main__":
    # Ici, nous plaçons tous les fichiers uploadés dans le préfixe "processed" sur GCS.
    upload_recursively(BUCKET_NAME, LOCAL_ROOT, "processed")
