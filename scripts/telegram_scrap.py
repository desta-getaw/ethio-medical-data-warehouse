import os
import json
import asyncio
import logging
from datetime import datetime
# Make sure to install 'telethon' using pip before running this script:
# pip install telethon

from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')

# Channels to scrape (text + media info)
CHANNELS = [
    'CheMed123',
    'lobelia4cosmetics',
    'tikvahpharma',
    'medicine',

    # Additional channels from https://et.tgstat.com/medicine could be added here as usernames or IDs
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def scrape_channel(client, channel_name):
    logging.info(f"Scraping channel: {channel_name}")
    today = datetime.utcnow().strftime('%Y-%m-%d')
    output_dir = f"data/raw/telegram_messages/{today}"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{channel_name}.json")

    messages_data = []

    try:
        async for message in client.iter_messages(channel_name):
            msg = {
                "id": message.id,
                "date": message.date.isoformat(),
                "text": message.message,
                "media": None,
                "has_photo": False,
            }
            if message.media:
                msg["media"] = str(message.media)
                if message.photo:
                    msg["has_photo"] = True
            messages_data.append(msg)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(messages_data, f, ensure_ascii=False, indent=2)

        logging.info(f"Saved {len(messages_data)} messages from {channel_name} to {output_file}")

    except Exception as e:
        logging.error(f"Failed to scrape {channel_name}: {e}")

async def main():
    async with TelegramClient('telegram_session', API_ID, API_HASH) as client:
        for ch in CHANNELS:
            await scrape_channel(client, ch)

if __name__ == '__main__':
    asyncio.run(main())
