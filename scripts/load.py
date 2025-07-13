import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

def load_json_to_postgres(json_file, table_name):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
        host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()

    # Create table if not exists (simple example)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS raw.{table_name} (
            id BIGINT PRIMARY KEY,
            date TIMESTAMP,
            text TEXT,
            media TEXT,
            has_photo BOOLEAN
        );
    """)

    for msg in data:
        cur.execute(f"""
            INSERT INTO raw.{table_name} (id, date, text, media, has_photo)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (
            msg['id'],
            msg['date'],
            msg.get('text'),
            msg.get('media'),
            msg.get('has_photo', False)
        ))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Loaded {len(data)} records into raw.{table_name}")

if __name__ == "__main__":
    # Example: loop over JSON files and load
    data_dir = "data/raw/telegram_messages/2025-07-13"
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            channel_name = filename.replace('.json', '')
            json_path = os.path.join(data_dir, filename)
            load_json_to_postgres(json_path, channel_name)
