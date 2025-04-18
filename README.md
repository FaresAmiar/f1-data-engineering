Problem Statement

In Formula 1, every millisecond on track can make the difference between victory and defeat. Teams generate vast amounts of data—from lap times and sector splits to tire choices and weather conditions—but it often remains:

Scattered across multiple, nested JSON files (Ergast API),

Uncleaned and unstandardized, making cross‑analysis (driver ↔ circuit ↔ season) cumbersome,

Ill‑suited for fast, ad‑hoc queries, lacking a dimensional model or fact tables,

Difficult to share in a self‑service, interactive format for engineers, strategists, and performance analysts.

How might we provide F1 teams with a unified, interactive data platform that enables them to:

Rank drivers by total points, podiums, and wins each season,

Track performance trends across the season (cumulative points and position changes race‑by‑race),

Compare circuit‑by‑circuit results (average points, number of victories) for each driver and constructor,

Benchmark constructors across all Grands Prix,

…so that race engineers and strategists can quickly spot performance patterns, simulate “what‑if” scenarios, and optimize race strategies in near real‑time?

This project addresses that challenge by delivering:

A Spark ingestion pipeline that flattens and denormalizes raw JSON into tabular NDJSON,

A BigQuery warehouse structured via dbt into staging, dimension, and fact tables,

Consolidated SQL views (vw_f1_dashboard, vw_season_driver_summary, etc.) ready for analysis,

An interactive Looker Studio dashboard that brings all these metrics to life—enabling any team member to explore, filter, and share F1 insights with a single click.


## 1. Create your Service Account

1. In the GCP Console → **IAM & Admin** → **Service Accounts** → **Create Service Account**.  
2. Grant it these roles:  
   - **BigQuery Admin**  
   - **BigQuery Metadata Viewer**  
   - **Storage Admin**  
3. Download the JSON key and place it at the root of this repo, named exactly:

sa.json

yaml
Copier
Modifier

---

## 2. Prepare your environment

At the root of the project, run:

```bash
cp /path/to/your/key.json sa.json
touch .env
```

Note: Terraform will populate your .env with:

TF_VAR_bucket

TF_VAR_region (must be europe-west1)

TF_VAR_project_id

TF_VAR_bq_dataset_name

Infrasture

Provision infrastructure with Terraform

A GCS bucket

A BigQuery dataset (and any required tables)

4. Launch the services via Docker Compose
bash
```
docker-compose up --build
```

If you run into errors or a service hangs, you can:

start each service in order:

bash
```
docker-compose up terraform
docker-compose up f1_ingestion
docker-compose up spark_job
docker-compose up f1_upload_processed
docker-compose up dbt
```

6. Import the Looker Studio dashboard
Open the template in Looker Studio:
https://lookerstudio.google.com/reporting/0ea4a7ef-cf5a-4a4c-b4bc-18eb4800d0e4

Click File → Make a copy.

Go to Resource → Manage added data sources → Replace data source and point it at your BigQuery dataset (TF_VAR_bq_dataset_name) and the view vw_f1_dashboard.

Finally, click Share → Manage access to grant your teammates Viewer or Editor rights, and enable “Allow viewers to make a copy” if you want them to fork it.

[F1_Data_Analysis.pdf](https://github.com/user-attachments/files/19813140/F1_Data_Analysis.pdf)
