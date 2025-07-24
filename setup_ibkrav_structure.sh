#!/bin/bash

set -e

# Crear estructura de carpetas Clean Architecture
mkdir -p ibkrav/{infrastructure,domain,application,interface} scripts tests data

# Crear __init__.py para paquetes Python
touch ibkrav/{__init__.py,infrastructure/__init__.py,domain/__init__.py,application/__init__.py,interface/__init__.py}

# Renombrar y mover archivos existentes si están presentes
if [[ -f ibkr_api.py ]]; then
  mv ibkr_api.py ibkrav/infrastructure/ibkr_client.py
fi

if [[ -f acciones_ibkr.py ]]; then
  mv acciones_ibkr.py ibkrav/domain/signals.py
fi

if [[ -f main.py ]]; then
  mv main.py scripts/main.py
fi

# Crear ejemplo de archivo main CLI
cat << 'EOF' > ibkrav/interface/cli.py
from ibkrav.application.trading_service import ejecutar_flujo_trading

def main():
    ejecutar_flujo_trading()

if __name__ == "__main__":
    main()
EOF

# Crear archivo de ejemplo en application
cat << 'EOF' > ibkrav/application/trading_service.py
def ejecutar_flujo_trading():
    print("Ejecutando estrategia de trading...")
    # Aquí importarías signals, ibkr_client, etc.
EOF

# Crear requirements.txt si no existe
if [[ ! -f requirements.txt ]]; then
  cat << 'REQ' > requirements.txt
ib_insync
pandas
python-dotenv
REQ
fi

# Crear .env.example para configurar conexión a IBKR
cat << 'EOF' > .env.example
IB_HOST=127.0.0.1
IB_PORT=7497
IB_CLIENT_ID=1
EOF

# Crear README básico si no existe
if [[ ! -f README.md ]]; then
  echo "# IBKRAV" > README.md
  echo "Proyecto reorganizado con Clean Architecture. Ejecuta con \`python ibkrav/interface/cli.py\`" >> README.md
fi

# Mensaje final
echo "✅ Estructura IBKRAV reorganizada con Clean Architecture"
echo "Ejecuta: python ibkrav/interface/cli.py para correr flujo principal"
