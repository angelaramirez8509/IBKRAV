from ibkrav.model import signals
from ibkrav.ibapi.client import IBKRClient
from ibkrav.view.terminal import mostrar_resultado
from ibkrav.view.telegram import enviar_mensaje_telegram
from ibkrav.model.signals import detectar_tendencia_alcista
import pandas as pd

def ejecutar():
    client = IBKRClient()
    client.conectar()
    symbol = "AAPL"
    datos = client.obtener_datos_historicos(symbol)

    # ✅ Convertir a DataFrame para análisis
    df = pd.DataFrame(datos)

    signal = signals.generar_signal(datos)
    mostrar_resultado(symbol, signal)
    enviar_mensaje_telegram(symbol, signal)

    if detectar_tendencia_alcista(df):
        print("🚀 Tendencia alcista fuerte. Revisar que el MA20 y MA40 se vean paralelas. Si el PM40 se aleja por encima estamos en zona cara")
        