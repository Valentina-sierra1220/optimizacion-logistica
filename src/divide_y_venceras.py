import json
import time

def verificar_capacidad(paq, cap, izq=0, der=None):
    if der is None: der = len(paq) - 1
    if izq > der: return True, 0
    if izq == der:
        peso = paq[izq].get("peso", 0)
        return peso <= cap, peso
    
    medio = (izq + der) // 2
    ok_izq, p_izq = verificar_capacidad(paq, cap, izq, medio)
    if not ok_izq: return False, 0
    
    ok_der, p_der = verificar_capacidad(paq, cap, medio + 1, der)
    if not ok_der: return False, 0
    
    return (p_izq + p_der) <= cap, p_izq + p_der

def algoritmo_divide_y_venceras(paquetes, camiones, repeticiones=100):
    capacidad_total = sum(c["capacidad"] for c in camiones)
    paquetes_ord = sorted(paquetes, key=lambda x: x["id"])
    
    # Medición con promedio para eliminar el ruido del sistema operativo
    t0 = time.perf_counter()
    for _ in range(repeticiones):
        factible, peso_total = verificar_capacidad(paquetes, capacidad_total)
    tiempo_total = (time.perf_counter() - t0) / repeticiones
    
    return {
        "metodo": "Divide y Vencerás",
        "factible": factible,
        "peso_total": peso_total,
        "tiempo_ejecucion": tiempo_total,
        "total_paquetes": len(paquetes_ord)
    }, paquetes_ord