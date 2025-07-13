import os

# Define the folder and file structure
structure = {
    ".env": "",
    ".gitignore": "# Ignore environment and data files\n.env\ndata/\nlogs/\n__pycache__/\n",
    "Dockerfile": "# Docker build instructions\n",
    "docker-compose.yml": "# Docker Compose configuration\n",
    "requirements.txt": "# Python dependencies\n",
    "README.md": "# Project Overview\n\nThis project extracts Telegram data, enriches it, models with dbt, and serves with FastAPI.\n",
    "scripts": {
        "scrape_telegram.py": "# Task 1: Scrape Telegram data\n",
        "load_raw_to_postgres.py": "# Task 2: Load raw data into PostgreSQL\n",
        "yolo_enrichment.py": "# Task 3: YOLO object detection and enrichment\n"
    },
    "telegram_dbt_project": {
        "models": {
            "staging": {
                "stg_telegram_messages.sql": "-- SQL for staging Telegram messages\n",
                "sources.yml": "# dbt sources config\n"
            },
            "marts": {
                "dim_channels.sql": "-- Dimension table: channels\n",
                "dim_dates.sql": "-- Dimension table: dates\n",
                "fct_messages.sql": "-- Fact table: messages\n",
                "fct_image_detections.sql": "-- Fact table: YOLO detections\n"
            }
        },
        "tests": {
            "assert_positive_message_length.sql": "-- Custom test\n"
        },
        "dbt_project.yml": "# dbt project configuration\n",
        "profiles.yml": "# dbt profiles configuration\n"
    },
    "api": {
        "main.py": "# FastAPI app\n",
        "database.py": "# DB connection\n",
        "schemas.py": "# Pydantic models\n",
        "crud.py": "# CRUD operations\n"
    },
    "dagster_pipeline.py": "# Dagster pipeline definition\n",
    "repository.py": "# Dagster repository definition\n",
    "data": {
        "raw": {
            "telegram_messages": {
                "YYYY-MM-DD": {
                    "channel_id.jsonl": ""
                }
            },
            "images": {
                "channel_id": {
                    "message_id.jpg": ""
                }
            }
        }
    },
    "docs": {
        "report.pdf": "",
        "pipeline_diagram.png": "",
        "star_schema_diagram.png": ""
    },
    "logs": {}
}

def create_structure(base_path, struct):
    for name, content in struct.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            # Make sure parent directory exists
            os.makedirs(os.path.dirname(path), exist_ok=True)
            # Create file with optional starter content
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    base_directory = "ethio-medical-data-warehouse"  # Change this to your preferred root folder name
    os.makedirs(base_directory, exist_ok=True)
    create_structure(base_directory, structure)
    print(f"✅ Project structure created under '{base_directory}/'")
