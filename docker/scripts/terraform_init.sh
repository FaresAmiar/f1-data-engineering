#!/bin/sh
set -e

echo "Starting Terraform provisioning script..."

# Afficher le contenu du dossier /scripts (pour debug)
ls -la /scripts

# Afficher le contenu du répertoire de travail actuel
ls -la .

echo "Dossier /workspace :"
ls -la /workspace

cat .env

if [ -f /workspace/.env ]; then
  echo "Exporting env variables from /workspace/.env"
  export $(grep -v '^#' /workspace/.env | xargs)
else
  echo "/workspace/.env not found"
fi

echo "Variables TF_VAR_ :"
env | grep TF_VAR_ || true

echo "Project ID from env: $TF_VAR_project_id"

sh /get_project_id.sh

# Afficher le contenu du fichier de variables d'environnement

echo "Changing directory to 'terraform'..."
cd terraform

echo "Now in directory: $(pwd)"

# Optionnel : exécuter le script get_project_id.sh pour mettre à jour les variables si besoin
# sh ../scripts/get_project_id.sh

terraform init
echo "Terraform initialized successfully."

terraform apply -auto-approve
echo "Terraform applied successfully."

