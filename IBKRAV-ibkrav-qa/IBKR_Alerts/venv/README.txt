#Ejecución de Dockerfile
docker build -t ibkr_alerts .
docker run --rm ibkr_alerts

venv para poder instalar pip
python -m venv venv
source venv/bin/activate  # Linux o Mac
# o
venv\Scripts\activate     # Windows

pip install ib_insync
pip install pandas
pip install python-telegram-bot
pip install schedule
pip install ta
