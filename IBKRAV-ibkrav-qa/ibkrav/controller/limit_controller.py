from ibkrav.model.limit_price import calcular_precio_limite
from ibkrav.view.limit_prompt import solicitar_datos_usuario, mostrar_resultado

def ejecutar_calculo_limite():
    datos = solicitar_datos_usuario()
    resultado = calcular_precio_limite(*datos)
    mostrar_resultado(resultado)
