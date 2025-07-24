from ib_insync import IB, Stock

class IBKRClient:
    def __init__(self, host='127.0.0.1', port=7497, client_id=1):
        self.ib = IB()
        self.host = host
        self.port = port
        self.client_id = client_id

    def conectar(self):
        try:
            self.ib.connect(self.host, self.port, clientId=self.client_id)
            print("✅ Conectado a IBKR")
        except Exception as e:
            print(f"❌ Error al conectar: {e}")

    def obtener_datos_historicos(self, symbol):
        contrato = Stock(symbol, 'SMART', 'USD')
        self.ib.qualifyContracts(contrato)
        barras = self.ib.reqHistoricalData(
            contrato,
            endDateTime="",
            durationStr="1 D",
            barSizeSetting="5 mins",
            whatToShow="MIDPOINT",
            useRTH=True,
            formatDate=1
        )
        return barras
