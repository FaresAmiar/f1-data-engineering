# F1 Analytics Dashboard Quickstart

---

## Problem Statement

In Formula 1, every millisecond on the track can make the difference between victory and defeat. Teams generate vast amounts of data—from lap times and sector splits to tire choices and weather conditions—but it often remains:

- **Scattered** across multiple, nested JSON files (Ergast API)  
- **Uncleaned and unstandardized**, making cross‑analysis (driver ↔ circuit ↔ season) cumbersome  
- **Ill‑suited for fast, ad‑hoc queries**, lacking a dimensional model or fact tables  
- **Difficult to share** in a self‑service, interactive format for engineers, strategists, and performance analysts  

**How might we** provide F1 teams with a unified, interactive data platform that enables them to:

1. **Rank drivers** by total points, podiums, and wins each season  
2. **Track performance trends** across the season (cumulative points and position changes race‑by‑race)  
3. **Compare circuit‑by‑circuit results** (average points, number of victories) for each driver and constructor  
4. **Benchmark constructors** across all Grands Prix  

…so that race engineers and strategists can quickly spot performance patterns, simulate “what‑if” scenarios, and optimize race strategies in near real‑time?

This project addresses that challenge by delivering:

- A **Spark ingestion pipeline** that flattens and denormalizes raw JSON into tabular NDJSON  
- A **BigQuery warehouse** structured via dbt into staging, dimension, and fact tables  
- **Consolidated SQL views** (`vw_f1_dashboard`) ready for analysis  
- An **interactive Looker Studio dashboard** that brings all these metrics to life—enabling any team member to explore, filter, and share F1 insights with a single click  

---

## 1. Create your Service Account

1. In the GCP Console → **IAM & Admin** → **Service Accounts** → **Create Service Account**  
2. Grant it these roles:  
   - **BigQuery Admin**  
   - **BigQuery Metadata Viewer**  
   - **Storage Admin**  
3. Download the JSON key and place it at the root of this repo, named exactly:  
   ```text
   sa.json
   ```

---

## 2. Prepare your environment

At the root of the project, run:

```bash
cp /path/to/your/key.json sa.json
touch .env
```

> **Note:** Terraform will populate your `.env` with:  
> - `TF_VAR_bucket`  
> - `TF_VAR_region` (must be **europe-west1**)  
> - `TF_VAR_project_id`  
> - `TF_VAR_bq_dataset_name`

---

### Infrastructure


This will create:  
- A **GCS bucket**  
- A **BigQuery dataset** (and any required tables)  
- Auto‑populate your `.env` with the correct values

---

## 4. Launch the Services via Docker Compose

```bash
docker-compose up --build
```

If you run into errors or a service hangs, either:

```bash
docker-compose restart
```

or start each service in order:

```bash
docker-compose up terraform
docker-compose up f1_ingestion
docker-compose up spark_job
docker-compose up f1_upload_processed
docker-compose up dbt
```

---

## 5. Verify your services are running

```bash
docker-compose ps
```

---

## 6. Import the Looker Studio Dashboard

1. Open the template in Looker Studio:  
   https://lookerstudio.google.com/reporting/0ea4a7ef-cf5a-4c4c-b4bc-18eb4800d0e4  
2. Click **File → Make a copy**  
3. Go to **Resource → Manage added data sources → Replace data source** and point it at your BigQuery dataset (`TF_VAR_bq_dataset_name`) and the view `vw_f1_dashboard`  
4. Click **Share → Manage access** to grant your teammates Viewer or Editor rights, and enable **“Allow viewers to make a copy”** if you want them to fork it  

---

You’re now ready to explore F1 race results, driver standings, and track‑by‑track performance!

![image](https://github.com/user-attachments/assets/aae2affc-e588-4ffb-ab82-cd14d5c64ab1)
![image](https://github.com/user-attachments/assets/79121034-58f2-44f3-9c5a-6b9a876b1601)
![image](https://github.com/user-attachments/assets/f7f6c679-5ed2-46fb-b198-935c04fa8800)
