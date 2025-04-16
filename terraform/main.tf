# 1. Création du bucket
resource "google_storage_bucket" "f1_data" {
  name          = var.bucket_name
  location      = var.region
  storage_class = "STANDARD"
  force_destroy = true

}

# 2. Création du dataset BigQuery
resource "google_bigquery_dataset" "f1_dataset" {
  dataset_id = var.bq_dataset_name
  project    = var.project_id
  location   = var.region
}



# Création des tables BigQuery externes

# resource "google_bigquery_table" "race_results_external" {
#   dataset_id = var.bq_dataset_name
#   table_id   = "race_results"
#   depends_on = [google_bigquery_dataset.f1_dataset]
#
#   external_data_configuration {
#     source_uris   = ["gs://${var.bucket_name}/f1_results_*.json"]
#     source_format = "NEWLINE_DELIMITED_JSON"
#     autodetect    = true
#   }
# }
#
# resource "google_bigquery_table" "results_raw_external" {
#   dataset_id = var.bq_dataset_name
#   table_id   = "results_raw"
#   depends_on = [google_bigquery_dataset.f1_dataset]
#
#   external_data_configuration {
#     source_uris   = ["gs://${var.bucket_name}/results_raw.json"]
#     source_format = "NEWLINE_DELIMITED_JSON"
#     autodetect    = true
#   }
# }
#
# resource "google_bigquery_table" "drivers_raw_external" {
#   dataset_id = var.bq_dataset_name
#   table_id   = "drivers_raw"
#   depends_on = [google_bigquery_dataset.f1_dataset]
#
#   external_data_configuration {
#     source_uris   = ["gs://${var.bucket_name}/drivers_raw.json"]
#     source_format = "NEWLINE_DELIMITED_JSON"
#     autodetect    = true
#   }
# }
