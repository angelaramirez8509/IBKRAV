from ibkrav.model import signals
from ibkrav.ibapi.client import IBKRClient
from ibkrav.view.terminal import mostrar_resultado
from ibkrav.view.telegram import enviar_mensaje_telegram

def ejecutar():
    client = IBKRClient()
    client.conectar()
    symbol = "AAPL"
    datos = client.obtener_datos_historicos(symbol)
    signal = signals.generar_signal(datos)
    mostrar_resultado(symbol, signal)
    enviar_mensaje_telegram(symbol, signal)
