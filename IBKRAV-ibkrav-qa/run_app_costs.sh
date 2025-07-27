#!/bin/bash
cd "$(dirname "$0")"

echo ""
echo "🛠 Menú de herramientas IBKRAV"
echo "-----------------------------"
echo "1. Ejecutar CLI de precio límite"
echo "2. Lanzar GUI modo oscuro (Tkinter)"
echo "3. Salir"
read -p "Elige una opción [1-3]: " opcion

if [ "$opcion" == "1" ]; then
    python run_limit.py
elif [ "$opcion" == "2" ]; then
    python -m ibkrav.gui.limit_price_gui
else
    echo "👋 Saliendo..."
fi
