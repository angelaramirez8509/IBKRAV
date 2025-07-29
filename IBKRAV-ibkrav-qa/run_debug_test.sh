#!/bin/bash

# Activar entorno virtual si existe
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✅ Entorno virtual activado"
else
    echo "⚠️ No se encontró el entorno virtual en venv/"
fi

# Ejecutar test de gráfica
echo "🚀 Ejecutando prueba de gráfico..."
python debug_test.py
