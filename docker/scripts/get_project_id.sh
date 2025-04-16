#!/bin/bash
set -e

echo "Starting script..."

# Récupérer le project_id du fichier JSON de Service Account
PROJECT_ID=$(jq -r '.project_id' /workspace/sa.json)

# Générer un nom de bucket aléatoire
BUCKET_NAME="f1-data-bucket-$(uuidgen)"

# Définir la région manuellement (choisis celle qui te convient, par exemple "europe-west1" ou "us-central1")
REGION="europe-west1"

# Générer un nom de dataset aléatoire, par exemple en ajoutant un UUID
BQ_DATASET_NAME="f1_dataset_$(uuidgen | tr '-' '_')"

# Mettre à jour le fichier .env uniquement si les variables ne sont pas déjà définies

grep -q "^TF_VAR_project_id=" /workspace/.env || echo "TF_VAR_project_id=$PROJECT_ID" >> /workspace/.env
grep -q "^TF_VAR_bucket_name=" /workspace/.env || echo "TF_VAR_bucket_name=$BUCKET_NAME" >> /workspace/.env
grep -q "^TF_VAR_region=" /workspace/.env || echo "TF_VAR_region=$REGION" >> /workspace/.env
grep -q "^TF_VAR_bq_dataset_name=" /workspace/.env || echo "TF_VAR_bq_dataset_name=$BQ_DATASET_NAME" >> /workspace/.env

echo "Script executed successfully."
