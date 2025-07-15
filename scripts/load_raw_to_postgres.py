import os
import json
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_batch

def ensure_table_structure(conn):
    """Ensure the table exists with all required columns"""
    with conn.cursor() as cursor:
        try:
            # Create schema and basic table structure
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS raw;
                
                CREATE TABLE IF NOT EXISTS raw.telegram_messages (
                    id BIGINT PRIMARY KEY,
                    message_text TEXT,
                    date TIMESTAMP,
                    channel VARCHAR(255),
                    other_fields JSONB,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """)
            
            # Add updated_at column if it doesn't exist
            cursor.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns 
                        WHERE table_schema='raw' 
                        AND table_name='telegram_messages' 
                        AND column_name='updated_at'
                    ) THEN
                        ALTER TABLE raw.telegram_messages 
                        ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();
                    END IF;
                END$$;
            """)
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error ensuring table structure: {e}")
            return False

def process_file(cursor, file_path):
    """Process a single JSON file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            messages = json.load(f)
            
        batch_data = []
        for message in messages:
            batch_data.append((
                message.get('id'),
                message.get('message'),
                message.get('date'),
                message.get('channel'),
                json.dumps(message)
            ))
        
        execute_batch(
            cursor,
            """INSERT INTO raw.telegram_messages 
               (id, message_text, date, channel, other_fields)
               VALUES (%s, %s, %s, %s, %s)
               ON CONFLICT (id) DO UPDATE SET
                   message_text = EXCLUDED.message_text,
                   date = EXCLUDED.date,
                   channel = EXCLUDED.channel,
                   other_fields = EXCLUDED.other_fields,
                   updated_at = NOW()""",
            batch_data,
            page_size=100
        )
        
        return len(batch_data), cursor.rowcount
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {file_path}: {e}")
        return 0, 0
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0, 0

def load_telegram_messages():
    conn = None
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname="ethiomedica",
            user="postgres",
            password="1221",
            host="localhost",
            port="5432"
        )
        
        # Ensure table structure exists
        if not ensure_table_structure(conn):
            return

        data_dir = "data/raw/telegram_messages"
        stats = {
            'processed_files': 0,
            'total_records': 0,
            'inserted': 0,
            'updated': 0,
            'failed_files': 0
        }

        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    cursor = conn.cursor()
                    try:
                        records, affected = process_file(cursor, file_path)
                        conn.commit()
                        
                        stats['processed_files'] += 1
                        stats['total_records'] += records
                        if affected > 0:
                            stats['inserted'] += (records - (affected - records))
                            stats['updated'] += (affected - records)
                    except Exception as e:
                        conn.rollback()
                        stats['failed_files'] += 1
                        print(f"Failed to process {file_path}: {e}")
                    finally:
                        cursor.close()

        print("\nProcessing complete:")
        print(f"- Successfully processed files: {stats['processed_files']}")
        print(f"- Failed files: {stats['failed_files']}")
        print(f"- Total records processed: {stats['total_records']}")
        print(f"- New records inserted: {stats['inserted']}")
        print(f"- Existing records updated: {stats['updated']}")

    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    load_telegram_messages()