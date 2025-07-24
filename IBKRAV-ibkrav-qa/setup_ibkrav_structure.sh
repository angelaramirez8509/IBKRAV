#!/bin/bash

set -e

# Crear estructura de carpetas estilo MVC
mkdir -p ibkrav/{model,view,controller,ibapi} resultados tests

# Crear __init__.py para paquetes Python
touch ibkrav/{__init__.py,model/__init__.py,view/__init__.py,controller/__init__.py,ibapi/__init__.py}

# Mover archivos existentes al nuevo esquema
[[ -f acciones_ibkr.py ]] && mv acciones_ibkr.py ibkrav/model/signals.py
[[ -f ibkr_api.py ]] && mv ibkr_api.py ibkrav/ibapi/client.py
[[ -f main.py ]] && mv main.py ibkrav/controller/trading_controller.py

# Crear vista de terminal
cat << 'EOF' > ibkrav/view/terminal.py
def mostrar_resultado(symbol, signal):
    print(f"Resultado para {symbol}: {signal}")
EOF

# Crear vista de telegram
cat << 'EOF' > ibkrav/view/telegram.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

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
EOF

# Crear archivo controlador adaptado
cat << 'EOF' > ibkrav/controller/trading_controller.py
from ibkrav.model import signals
from ibkrav.ibapi.client import IBKRClient
from ibkrav.view.terminal import mostrar_resultado
from ibkrav.view.telegram import enviar_mensaje_telegram

def ejecutar():
    client = IBKRClient()
    client.conectar()
    symbol = "AAPL"
    datos = client.obtener_datos_historicos(symbol)
    signal = signals.generar_signal(datos)
    mostrar_resultado(symbol, signal)
    enviar_mensaje_telegram(symbol, signal)
EOF

# Crear clase cliente IBKR
cat << 'EOF' > ibkrav/ibapi/client.py
from ib_insync import IB, Stock

class IBKRClient:
    def __init__(self, host='127.0.0.1', port=7497, client_id=1):
        self.ib = IB()
        self.host = host
        self.port = port
        self.client_id = client_id

    def conectar(self):
        try:
            self.ib.connect(self.host, self.port, clientId=self.client_id)
            print("✅ Conectado a IBKR")
        except Exception as e:
            print(f"❌ Error al conectar: {e}")

    def obtener_datos_historicos(self, symbol):
        contrato = Stock(symbol, 'SMART', 'USD')
        self.ib.qualifyContracts(contrato)
        barras = self.ib.reqHistoricalData(
            contrato,
            endDateTime="",
            durationStr="1 D",
            barSizeSetting="5 mins",
            whatToShow="MIDPOINT",
            useRTH=True,
            formatDate=1
        )
        return barras
EOF

# Crear modelo señales
cat << 'EOF' > ibkrav/model/signals.py
def generar_signal(datos):
    if not datos:
        return "NO DATA"
    if datos[-1].close > datos[0].close:
        return "BUY"
    return "SELL"
EOF

# Crear entrypoint de ejecución
cat << 'EOF' > run.py
from ibkrav.controller.trading_controller import ejecutar

ejecutar()
EOF

# Crear requirements.txt si no existe
[[ ! -f requirements.txt ]] && echo -e "ib_insync\npandas\npython-dotenv\nrequests" > requirements.txt

# Crear .env.example para conexión a IBKR y Telegram
cat << 'EOF' > .env.example
IB_HOST=127.0.0.1
IB_PORT=7497
IB_CLIENT_ID=1
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_chat_id
EOF

# Crear README básico si no existe
[[ ! -f README.md ]] && echo -e "# IBKRAV MVC\n\nEjecuta: python run.py" > README.md

# Crear entorno virtual e instalar dependencias
if [[ ! -d venv ]]; then
  python3 -m venv venv
  source venv/bin/activate
  echo "📦 Instalando dependencias..."
  pip install --upgrade pip
  pip install -r requirements.txt
  echo "✅ Entorno virtual creado e instalado"
else
  echo "ℹ️ Entorno virtual ya existe (venv/)"
fi

# Mensaje final
echo "✅ Proyecto reorganizado con patrón MVC"
echo "Ejecuta:
  source venv/bin/activate
  python run.py"
