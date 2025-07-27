def solicitar_datos_usuario():
    print("\n📈 Calculadora de Precio Límite (Opciones CALL)\n")
    contratos = int(input("🔹 Cantidad de contratos: "))
    costo = float(input("🔹 Costo por contrato (ej. 0.30): "))
    usar_auto = input("¿Deseas calcular comisiones automáticamente? (s/n): ").lower() == 's'
    comision_manual = float(input("🔹 Ingrese la comisión total manual: ")) if not usar_auto else 0.0
    multiplicador = float(input("🔹 Multiplicador de ganancia deseado (ej. 2 para 100%): "))
    return contratos, costo, usar_auto, comision_manual, multiplicador

def mostrar_resultado(resultado: dict):
    print("\n📊 Resultado del Cálculo:")
    for k, v in resultado.items():
        print(f"{k.replace('_', ' ').capitalize()}: ${v}")
