import os
import requests
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=env_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def enviar_mensaje_telegram(symbol, signal):
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ No hay configuración de Telegram")
        return
    mensaje = f"Signal para {symbol}: {signal}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(url, data={"chat_id": CHAT_ID, "text": mensaje})
        if response.status_code == 200:
            print("📨 Mensaje enviado por Telegram")
        else:
            print(f"❌ Error Telegram: {response.text}")
    except Exception as e:
        print(f"❌ Error al enviar mensaje: {e}")
