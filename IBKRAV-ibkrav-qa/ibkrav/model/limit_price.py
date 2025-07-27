def calcular_precio_limite(
    contratos,
    costo_por_contrato,
    usar_comision_auto=True,
    comision_manual=0.0,
    multiplicador=2.0,
    comision_fija=7.0,
    comision_por_contrato=1.25
):
    inversion = contratos * costo_por_contrato

    if usar_comision_auto:
        comision_total = comision_fija + comision_por_contrato * contratos
    else:
        comision_total = comision_manual

    total_invertido = inversion + comision_total
    costo_unitario = total_invertido / contratos
    precio_limite = costo_unitario * multiplicador

    return {
        "inversion_neta": round(inversion, 2),
        "comisiones": round(comision_total, 2),
        "total_invertido": round(total_invertido, 2),
        "costo_unitario": round(costo_unitario, 2),
        "precio_limite": round(precio_limite, 2),
    }
