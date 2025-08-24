# telegram_alerts.py
# Requiere: python-telegram-bot>=20.0
import asyncio
import os, requests
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()  # Cargar variables desde .env

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates", timeout=10)
r.raise_for_status()
for u in r.json().get("result", []):
    chat = u["message"]["chat"]
    print(chat["id"], chat.get("title") or chat.get("username") or chat.get("first_name"))

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
