# ibkrav/ibapi/ibkr_client.py
from ib_insync import IB, Stock, util
import pandas as pd
import os

class IBKRClient:
    def __init__(self, host='127.0.0.1', port=7497, clientId=1):
        self.ib = IB()
        self.host, self.port, self.clientId = host, port, clientId

    def conectar(self):
        self.ib.connect(self.host, self.port, clientId=self.clientId)

    def obtener_datos_historicos(self, symbol, duration='30 D', bar_size='1 hour'):
        contrato = Stock(symbol, 'SMART', 'USD')
        self.ib.qualifyContracts(contrato)
        barras = self.ib.reqHistoricalData(
            contrato,
            endDateTime='',
            durationStr=duration,
            barSizeSetting=bar_size,
            whatToShow='TRADES',
            useRTH=True
        )
        df = util.df(barras)
        df = df.set_index('date').loc[:, ['open','high','low','close','volume']]
        return df
