# ibkrav/view/telegram_utils.py

import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv
from pathlib import Path

# Carga variables del entorno
env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=env_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("❌ Faltan BOT_TOKEN o CHAT_ID en el .env")

bot = Bot(token=BOT_TOKEN)

async def enviar_telegram(texto: str):
    await bot.send_message(chat_id=CHAT_ID, text=texto)

if __name__ == "__main__":
    print("✅ Bot inicializado correctamente.")
    asyncio.run(enviar_telegram("🚀 Bot funcionando correctamente."))
