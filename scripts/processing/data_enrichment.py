import os
from ultralytics import YOLO
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Database connection
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def enrich_images():
    """Detects objects in images and stores the results in the database."""
    model = YOLO('yolov8n.pt')  # Load a pretrained model
    image_dir = 'data/raw/images'
    detection_results = []

    for root, _, files in os.walk(image_dir):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                message_id = os.path.splitext(file)[0]
                results = model(image_path)

                for result in results:
                    for box in result.boxes:
                        detection_results.append({
                            'message_id': int(message_id),
                            'detected_object_class': model.names[int(box.cls)],
                            'confidence_score': float(box.conf)
                        })

    if detection_results:
        df = pd.DataFrame(detection_results)
        df.to_sql('fct_image_detections', engine, if_exists='append', index=False)
        print(f"Enriched {len(df)} images.")

if __name__ == "__main__":
    enrich_images()