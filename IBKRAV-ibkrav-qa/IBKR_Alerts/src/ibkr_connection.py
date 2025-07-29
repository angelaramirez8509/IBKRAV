# ibkr_connection.py
from ib_insync import IB

def connect_ibkr():
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)  # Ajusta puerto si usas IB Gateway
    return ib
