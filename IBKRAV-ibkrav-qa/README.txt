#Ejecución de Dockerfile
docker build -t ibkr_alerts .
docker run --rm ibkr_alerts

#ejecutar el bash
chmod +x setup_ibkrav_structure.sh
./setup_ibkrav_structure.sh


venv para poder instalar pip


python -m venv venv
source venv/bin/activate  # Linux o Mac
# o
venv\Scripts\activate     # Windows


source venv/bin/activate

python3 run.py


pip install ib_insync
pip install pandas
pip install python-telegram-bot
pip install schedule
pip install ta
