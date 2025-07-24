def generar_signal(datos):
    if not datos:
        return "NO DATA"
    if datos[-1].close > datos[0].close:
        return "BUY"
    return "SELL"
