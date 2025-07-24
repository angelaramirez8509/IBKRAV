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

# Crear archivo controlador adaptado
cat << 'EOF' > ibkrav/controller/trading_controller.py
from ibkrav.model import signals
from ibkrav.ibapi.client import IBKRClient
from ibkrav.view.terminal import mostrar_resultado

def ejecutar():
    client = IBKRClient()
    client.conectar()
    symbol = "AAPL"
    datos = client.obtener_datos_historicos(symbol)
    signal = signals.generar_signal(datos)
    mostrar_resultado(symbol, signal)
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
[[ ! -f requirements.txt ]] && echo -e "ib_insync\npandas\npython-dotenv" > requirements.txt

# Crear .env.example para conexión a IBKR
cat << 'EOF' > .env.example
IB_HOST=127.0.0.1
IB_PORT=7497
IB_CLIENT_ID=1
EOF

# Crear README básico si no existe
[[ ! -f README.md ]] && echo -e "# IBKRAV MVC\n\nEjecuta: python run.py" > README.md

# Mensaje final
echo "✅ Proyecto reorganizado con patrón MVC"
echo "Ejecuta con: python run.py"
