# telegram_alerts.py
# Requiere: python-telegram-bot>=20.0
import asyncio
import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()  # Cargar variables desde .env

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def send_telegram(message: str):
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

def send_telegram_sync(message: str):
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(send_telegram(message))
    except RuntimeError:
        asyncio.run(send_telegram(message))

if __name__ == "__main__":
    send_telegram_sync("🚀 Prueba de alerta Telegram desde Python")
