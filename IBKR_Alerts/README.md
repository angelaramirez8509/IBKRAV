# IBKRAV MVC
# Ejecutar la app
#escribir /start desde el chat que se creó en Telegram

./setup_ibkr_alerts.sh

# Si hay que instalar alguna nueva libraria
# 1) Activar venv y mostrar rutas
source venv/bin/activate
which python; which pip
python -m pip --version

# 2) Instalar deps del proyecto
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 3) Verificar que requests está en ESTE intérprete
python - <<'PY'
import sys
try:
    import requests
    print("OK requests", requests.__version__, "PY:", sys.executable)
except Exception as e:
    print("FALTA requests:", e, "PY:", sys.executable)
PY

# NOTA: Cuando cambia el token del chatbot no cambia el chat_id 