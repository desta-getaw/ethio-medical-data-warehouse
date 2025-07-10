# 📦 Telegram Medical Data Analytics Pipeline

An end-to-end data pipeline project for analyzing Telegram channels covering Ethiopian medical businesses.  
Developed as part of the **10 Academy AI Mastery Program - Week 7 Challenge**.

---

## 🧠 **Business Understanding**

Ethiopia's medical and pharmaceutical market is vibrant but fragmented. Valuable data about products, prices, promotions, and trends is often shared publicly across Telegram channels. Our business goal is to **convert this raw, unstructured data into actionable insights** to answer questions like:

- What are the top 10 most frequently mentioned medical products?
- How does product price or availability change across channels?
- Which channels share more visual content (images of pills, creams, etc.)?
- What are daily and weekly posting trends?

By answering these, we help stakeholders better understand market dynamics, consumer demand, and competitive positioning.

---

## 🎯 **Project Objective**

To design and build a modern, production-ready **data product** that:
✅ Collects and stores raw Telegram data (text + images).  
✅ Cleans, models, and enriches data into a dimensional star schema.  
✅ Exposes insights via an API.  
✅ Automates the process with robust orchestration tools.  
✅ Follows best practices in environment management, containerization, and reproducibility.

---

## 🛠 **Solution Overview & Key Technologies**

- **Telegram API + Telethon**: Scraping data and media from target channels.
- **PostgreSQL**: Central data warehouse for structured storage.
- **dbt (Data Build Tool)**: Transform raw data into clean, analytical models.
- **YOLOv8 (Ultralytics)**: Detect objects in images to enrich data context.
- **FastAPI**: Expose data insights via a lightweight analytical API.
- **Dagster**: Orchestrate the pipeline and schedule automated runs.
- **Docker**: Containerize application and database for consistent deployment.
- **.env + python-dotenv**: Securely manage secrets and configs.

---

## 📂 **Project Structure (high-level)**

```plaintext
telegram-medical-pipeline/
├── app/                # Python modules (scraper, API, config, etc.)
├── data/               # Raw & processed data lake (excluded from git)
├── dbt/                # Data transformation models
├── docker/             # Docker-specific files (if needed)
├── scripts/            # Utility scripts (e.g., db load, enrichment)
├── .env                # Environment variables (never committed)
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 📌 **Detailed Task Breakdown & Rationale**

### ✅ Task 0 – Project Setup & Environment Management

**Activities:**
- Initialize Git repository & create `.gitignore` to protect sensitive files.
- Define `requirements.txt` to track Python dependencies.
- Write `Dockerfile` & `docker-compose.yml` to containerize the Python environment + PostgreSQL database.
- Store credentials (Telegram API keys, DB passwords) in a `.env` file (excluded from git).
- Use `python-dotenv` to load secrets into the app.

**Why:**  
Promotes reproducibility, makes deployment easy across environments, and keeps secrets secure.

---

### 📦 Task 1 – Data Scraping & Collection (Extract & Load)

**Activities:**
- Use Telethon to scrape text, media, and metadata from public Telegram channels like:
  - `https://t.me/lobelia4cosmetics`
  - `https://t.me/tikvahpharma`
- Organize raw JSON data in a partitioned data lake:
  - `data/raw/telegram_messages/YYYY-MM-DD/channel_name.json`
- Download and store images in a structured directory.
- Implement logging to track scraping process and handle rate limits.

**Business value:**  
Converts unstructured data from Telegram into a durable data lake, providing the raw material for analysis.

---

### 🏗 Task 2 – Data Modeling & Transformation (Transform)

**Activities:**
- Load raw JSON data into a PostgreSQL raw schema.
- Use dbt to clean and reshape data into:
  - **Staging models:** Basic cleaning & renaming.
  - **Mart models:** Analytical star schema:
    - `dim_channels` (channel metadata)
    - `dim_dates` (calendar data)
    - `fct_messages` (message facts linked by foreign keys)
- Implement dbt tests (unique, not_null) and custom business rules.
- Document models with `dbt docs`.

**Business value:**  
Makes data query-ready and trustworthy by enforcing structure and validation.

---

### 🧪 Task 3 – Data Enrichment with YOLO

**Activities:**
- Use `ultralytics` package with YOLOv8 to run object detection on collected images.
- Create a new fact table: `fct_image_detections` containing:
  - `message_id`, `detected_object_class`, `confidence_score`
- Link detections to message facts for richer analysis.

**Business value:**  
Adds visual context—e.g., detects types of products in images, enabling product-level insights.

---

### 🔍 Task 4 – Build Analytical API (FastAPI)

**Activities:**
- Build a FastAPI service to answer key business questions via endpoints:
  - `/api/reports/top-products?limit=10`
  - `/api/channels/{channel_name}/activity`
  - `/api/search/messages?query=paracetamol`
- Use Pydantic models for input/output validation.
- Connect API to transformed mart tables.

**Business value:**  
Allows business users and apps to query insights in real time, supporting data-driven decision making.

---

### 🔄 Task 5 – Pipeline Orchestration (Dagster)

**Activities:**
- Define Dagster ops and job covering steps:
  - Scraping, loading, transformations, enrichment.
- Launch Dagster UI (`dagster dev`) to monitor runs.
- Schedule daily or hourly automated pipeline execution.

**Business value:**  
Makes the pipeline production-ready: automated, maintainable, and observable.

---

## 🐳 **How to Run Locally with Docker**

```bash
docker-compose up --build
```

Stop containers:
```bash
docker-compose down
```

---

## 🔑 **.env Example**

```dotenv
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=strongpassword
POSTGRES_DB=telegram_db
```

> Never commit this file to version control!

---

## 📌 **Key Learning Outcomes**

✅ Modern ELT data architecture & layered data modeling.  
✅ Secure environment management & reproducible deployments.  
✅ Data enrichment using computer vision.  
✅ Building analytical APIs.  
✅ Pipeline orchestration and monitoring.

---

## 📅 **Timeline & Deliverables**

| Phase            | Deliverable                              | Due                        |
| ---------------- | ---------------------------------------- | ------------------------- |
| Interim          | GitHub repo with Tasks 0, 1, 2 complete  | Sunday 12 July 2025       |
| Final            | Blog post or PDF report, diagrams, API screenshots, GitHub code | Tuesday 15 July 2025 |

---

## 📊 **References & Further Reading**

- [Telethon Docs](https://docs.telethon.dev/)
- [dbt Documentation](https://docs.getdbt.com/)
- [Ultralytics YOLOv8](https://docs.ultralytics.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Dagster](https://dagster.io/)
- [Docker for Python](https://docs.docker.com/language/python/)

---

*Built with ❤️ by Kara Solutions team for the 10 Academy Week 7 Challenge*
