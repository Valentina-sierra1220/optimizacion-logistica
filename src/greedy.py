import itertools

def simular_ruta_valida(paquetes_camion, hora_inicio):
    """
    Verifica si existe al menos un orden de entrega (permutación) 
    que cumpla con las ventanas de tiempo exigidas para el conjunto de paquetes.
    """
    if not paquetes_camion:
        return True, hora_inicio
    
    mejor_tiempo = float('inf')
    for orden in itertools.permutations(paquetes_camion):
        tiempo_actual = hora_inicio
        valido = True
        for p in orden:
            tiempo_actual += p["tiempo_viaje"]
            if tiempo_actual > p["ventana_fin"]:
                valido = False
                break
            tiempo_actual = max(tiempo_actual, p["ventana_inicio"]) + p["tiempo_entrega"]
        
        if valido:
            if tiempo_actual < mejor_tiempo:
                mejor_tiempo = tiempo_actual
                
    if mejor_tiempo != float('inf'):
        return True, mejor_tiempo
    return False, float('inf')


def algoritmo_greedy(paquetes, camiones):
    """
    Algoritmo Voraz (Greedy):
    1. Organiza paquetes prioritariamente por inicio de ventana de atención.
    2. Asigna de forma irreversible cada paquete al primer camión factible.
    """
    # 1. ORGANIZAR: Ordenar los paquetes por ventana de inicio (prioridad voraz)
    paquetes_ordenados = sorted(
        paquetes, 
        key=lambda p: (p["ventana_inicio"], p["ventana_fin"])
    )
    
    asignacion = {}
    cargas_camiones = {c["id"]: 0 for c in camiones}
    paquetes_por_camion = {c["id"]: [] for c in camiones}
    
    pasos_evaluados = 0
    
    # 2. SELECCIONAR: Decisión local para cada paquete
    for paquete in paquetes_ordenados:
        asignado = False
        for camion in camiones:
            pasos_evaluados += 1
            c_id = camion["id"]
            
            # Condición 1: Capacidad suficiente
            if cargas_camiones[c_id] + paquete["peso"] <= camion["capacidad"]:
                # Condición 2: Ruta y horario válidos
                nuevos_paquetes = paquetes_por_camion[c_id] + [paquete]
                es_valido, _ = simular_ruta_valida(nuevos_paquetes, camion["hora_inicio"])
                
                if es_valido:
                    # Selección irreversible
                    asignacion[paquete["id"]] = c_id
                    cargas_camiones[c_id] += paquete["peso"]
                    paquetes_por_camion[c_id].append(paquete)
                    asignado = True
                    break # Pasa al siguiente paquete de inmediato
        
        if not asignado:
            # Si la heurística no encuentra camión válido para un paquete, retorna incompleto
            return None, pasos_evaluados

    return asignacion, pasos_evaluados