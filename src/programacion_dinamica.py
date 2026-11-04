import json
import time
from pathlib import Path


def asignar_paquetes_dp(paquetes, camiones, idx_paquete=0, estado_camiones=None, memo=None):
    # 1. Inicialización (Receta de clase)
    if memo is None:
        memo = {}
    if estado_camiones is None:
        # El estado inmutable: tupla de (capacidad_restante, tiempo_actual) por camión
        estado_camiones = tuple((c['capacidad'], c['hora_inicio']) for c in camiones)
        
    # 2. Caso base
    if idx_paquete >= len(paquetes):
        return 0, [] # 0 paquetes asignados, lista vacía de asignaciones
        
    # 3. ¿Ya lo calculé? (Clave del memo)[cite: 1]
    clave = (idx_paquete, estado_camiones)
    if clave in memo:
        return memo[clave]
        
    paquete = paquetes[idx_paquete]
    
    # 4. Calcular: Opción A - No asignar este paquete (Divide y vencerás)[cite: 1]
    max_paquetes, mejor_asignacion = asignar_paquetes_dp(
        paquetes, camiones, idx_paquete + 1, estado_camiones, memo
    )
    
    # Opción B - Intentar asignar el paquete a cada camión disponible
    for i, camion in enumerate(camiones):
        capacidad_restante, tiempo_actual = estado_camiones[i]
        
        # Verificar restricción de peso
        if capacidad_restante >= paquete['peso']:
            tiempo_llegada = max(tiempo_actual + paquete['tiempo_viaje'], paquete['ventana_inicio'])
            tiempo_fin_entrega = tiempo_llegada + paquete['tiempo_entrega']
            
            # Verificar ventanas de tiempo del paquete y del camión
            if tiempo_llegada <= paquete['ventana_fin'] and tiempo_fin_entrega <= camion['hora_fin']:
                # Crear nuevo estado inmutable para la recursión
                nuevo_estado = list(estado_camiones)
                nuevo_estado[i] = (capacidad_restante - paquete['peso'], tiempo_fin_entrega)
                
                # Llamada recursiva 
                paquetes_asignados, asignacion_recursiva = asignar_paquetes_dp(
                    paquetes, camiones, idx_paquete + 1, tuple(nuevo_estado), memo
                )
                
                # Actualizar si esta decisión maximiza los paquetes entregados
                if paquetes_asignados + 1 > max_paquetes:
                    max_paquetes = paquetes_asignados + 1
                    mejor_asignacion = [(paquete['id'], camion['id'])] + asignacion_recursiva
                    
    # 5. Guardar y retornar[cite: 1]
    memo[clave] = (max_paquetes, mejor_asignacion)
    return memo[clave]


