#!/bin/bash

# 🚀 Crear carpetas principales
mkdir -p IBKR_Alerts/{logs,src}

# 🚀 Navegar al proyecto
cd IBKR_Alerts

# 🚀 Inicializar entorno virtual
python3 -m venv venv
source venv/bin/activate

# 🚀 Crear requirements.txt con librerías base
cat <<EOL > requirements.txt
ib_insync
pandas
python-telegram-bot
EOL

# 🚀 Instalar requerimientos
pip install -r requirements.txt

# 🚀 Crear archivos base en src/
cat <<EOL > src/ibkr_connection.py
# ibkr_connection.py
from ib_insync import IB

def connect_ibkr():
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)  # Ajusta puerto si usas IB Gateway
    return ib
EOL

cat <<EOL > src/strategies.py
# strategies.py

# Aquí se implementarán las estrategias como check_moving_averages y check_gap_breakdown

EOL

cat <<EOL > src/telegram_alerts.py
# telegram_alerts.py

from telegram import Bot

TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'

def send_telegram(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)
EOL

cat <<EOL > src/main.py
# main.py

from ibkr_connection import connect_ibkr
from strategies import check_moving_averages, check_gap_breakdown

def main():
    ib = connect_ibkr()
    symbols = ['SPY', 'QQQ']
    for sym in symbols:
        check_moving_averages(ib, sym)
        check_gap_breakdown(ib, sym)
    ib.disconnect()

if __name__ == "__main__":
    main()
EOL

# 🚀 Crear carpeta de logs
mkdir -p logs

# 🚀 Mensaje final
echo "✅ Proyecto IBKR_Alerts inicializado. Activa el entorno con 'source venv/bin/activate' y ejecuta con 'python src/main.py'"
