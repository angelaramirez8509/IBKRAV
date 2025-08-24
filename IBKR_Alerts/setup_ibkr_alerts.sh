#!/bin/bash

set -e

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
  python3 -m venv venv
  source venv/bin/activate
  python3 "src/main.py"
fi


# Mensaje final
echo "✅ Proyecto reorganizado con patrón MVC"
echo "Ejecuta:
  source venv/bin/activate
  python3 src/main.py"
  # desactivar
  deactivate