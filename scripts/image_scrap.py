import os
import asyncio
import logging
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')

CHANNELS = [
    'CheMed123',
    'lobelia4cosmetics',
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def download_images(client, channel_name):
    logging.info(f"Downloading images from channel: {channel_name}")
    today = datetime.utcnow().strftime('%Y-%m-%d')
    output_dir = f"data/raw/telegram_images/{today}/{channel_name}"
    os.makedirs(output_dir, exist_ok=True)

    count = 0
    try:
        async for message in client.iter_messages(channel_name):
            if message.media and isinstance(message.media, MessageMediaPhoto):
                file_path = os.path.join(output_dir, f"{message.id}.jpg")
                if not os.path.exists(file_path):
                    await client.download_media(message, file=file_path)
                    count += 1

        logging.info(f"Downloaded {count} images from {channel_name} to {output_dir}")

    except Exception as e:
        logging.error(f"Error downloading images from {channel_name}: {e}")

async def main():
    async with TelegramClient('image_scraper_session', API_ID, API_HASH) as client:
        for ch in CHANNELS:
            await download_images(client, ch)

if __name__ == '__main__':
    asyncio.run(main())
