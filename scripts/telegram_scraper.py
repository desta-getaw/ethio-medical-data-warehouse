import os
import json
import asyncio
import logging
from datetime import datetime
from telethon import TelegramClient
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_scraper.log'),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()

# Configuration
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
SESSION_NAME = 'telegram_session'

CHANNELS = [
    'CheMed123',
    'lobelia4cosmetics',
    'tikvahpharma',
    'Thequorachannel',
]

async def scrape_channel(client, channel_name):
    """Scrape messages from a Telegram channel"""
    today = datetime.utcnow().strftime('%Y-%m-%d')
    output_dir = os.path.join("data", "raw", "telegram_messages", today)
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{channel_name}.json")

    messages_data = []
    try:
        async for message in client.iter_messages(channel_name, limit=1000):  # Limit to 1000 messages
            msg_data = {
                "id": message.id,
                "date": message.date.isoformat() if message.date else None,
                "text": message.text,
                "media": str(message.media) if message.media else None,
                "views": message.views if hasattr(message, 'views') else None,
            }
            messages_data.append(msg_data)

        # Save to JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(messages_data, f, ensure_ascii=False, indent=2)

        logging.info(f"Saved {len(messages_data)} messages from {channel_name}")

    except Exception as e:
        logging.error(f"Error scraping {channel_name}: {str(e)}")
        return False

    return True

async def main():
    """Main scraping function"""
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    try:
        await client.start()
        logging.info("Telegram client started successfully")
        
        for channel in CHANNELS:
            success = await scrape_channel(client, channel)
            if not success:
                logging.warning(f"Failed to complete scraping for {channel}")
                
    except Exception as e:
        logging.error(f"Fatal error in main: {str(e)}")
    finally:
        await client.disconnect()
        logging.info("Telegram client disconnected")

if __name__ == '__main__':
    asyncio.run(main())