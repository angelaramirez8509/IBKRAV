#!/bin/bash
cd "$(dirname "$0")"
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
fi

echo ""
echo "🛠 Menú de herramientas IBKRAV"
echo "-----------------------------"
echo "1. Ejecutar CLI de precio límite"
echo "2. Lanzar GUI modo oscuro (Tkinter)"
echo "3. Salir"
read -p "Elige una opción [1-3]: " opcion

if [ "$opcion" == "1" ]; then
    python3 run_limit.py
elif [ "$opcion" == "2" ]; then
    python3 -m ibkrav.gui.limit_price_gui
else
    echo "👋 Saliendo..."
fi
