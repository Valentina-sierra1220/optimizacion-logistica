import json
import time
from pathlib import Path

def asignar_paquetes_backtracking(paquetes, camiones):
    mejor_solucion = []
    max_paquetes = -1
    
    # Mantenemos el estado de los camiones para modificarlo y restaurarlo
    estado_camiones = {
        c['id']: {'capacidad': c['capacidad'], 'tiempo': c['hora_inicio']} 
        for c in camiones
    }

    # Función de poda: verifica si el movimiento es válido antes de hacerlo
    def es_valida(paquete, camion, estado_actual):
        if estado_actual['capacidad'] < paquete['peso']:
            return False
            
        tiempo_llegada = max(estado_actual['tiempo'] + paquete['tiempo_viaje'], paquete['ventana_inicio'])
        tiempo_fin_entrega = tiempo_llegada + paquete['tiempo_entrega']
        
        if tiempo_llegada > paquete['ventana_fin'] or tiempo_fin_entrega > camion['hora_fin']:
            return False
            
        return True

    def backtrack(idx_paquete, asignacion_actual):
        nonlocal mejor_solucion, max_paquetes
        
        # Guardar la mejor solución encontrada hasta el momento
        if len(asignacion_actual) > max_paquetes:
            max_paquetes = len(asignacion_actual)
            mejor_solucion = asignacion_actual[:]  # Guardar copia de la lista
            
        # Caso base: si ya revisamos todos los paquetes, retrocedemos
        if idx_paquete == len(paquetes):
            return
            
        paquete = paquetes[idx_paquete]
        
        # --- RAMA 1: No asignar este paquete (Explorar sin elegir) ---
        backtrack(idx_paquete + 1, asignacion_actual)
        
        # --- RAMA 2: Intentar asignar el paquete a cada camión ---
        for camion in camiones:
            estado = estado_camiones[camion['id']]
            
            # PODA: solo entramos si el movimiento respeta las reglas
            if es_valida(paquete, camion, estado):
                
                # Guardar el estado anterior para poder deshacer
                cap_ant = estado['capacidad']
                tiempo_ant = estado['tiempo']
                
                tiempo_llegada = max(estado['tiempo'] + paquete['tiempo_viaje'], paquete['ventana_inicio'])
                nuevo_tiempo = tiempo_llegada + paquete['tiempo_entrega']
                
                # 1. ELEGIR[cite: 3]
                estado['capacidad'] -= paquete['peso']
                estado['tiempo'] = nuevo_tiempo
                asignacion_actual.append((paquete['id'], camion['id']))
                
                # 2. EXPLORAR[cite: 3]
                backtrack(idx_paquete + 1, asignacion_actual)
                
                # 3. DESHACER (Backtrack)[cite: 3]
                estado['capacidad'] = cap_ant
                estado['tiempo'] = tiempo_ant
                asignacion_actual.pop()

    # Iniciar la recursión con el paquete 0 y una asignación vacía
    backtrack(0, [])
    return max_paquetes, mejor_solucion



def main():
    # Cambia esto por caso_mediano.txt o caso_grande.txt para probar la escalabilidad
    ruta_archivo = Path("datos/caso_grande.txt") 
    
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        datos = json.load(f)
        
    camiones = datos["camiones"]
    paquetes = datos["paquetes"]
    
    print("\n------------------------------")
    print(" OPTIMIZACION LOGISTICA")
    print(" BACKTRACKING")
    print("==============================")
    print(f"\nCantidad de camiones: {len(camiones)}")
    print(f"Cantidad de paquetes: {len(paquetes)}")
    
    inicio = time.perf_counter()
    max_paquetes, asignaciones = asignar_paquetes_backtracking(paquetes, camiones)
    tiempo = time.perf_counter() - inicio
    
    if max_paquetes == 0:
        print("\nNo existe una asignacion factible.")
    else:
        print(f"\nPaquetes entregados con éxito: {max_paquetes} de {len(paquetes)}")
        
    print(f"Tiempo de ejecución: {tiempo:.8f} segundos")
    
    entregas_por_camion = {c["id"]: [] for c in camiones}
    for id_paquete, id_camion in asignaciones:
        entregas_por_camion[id_camion].append(id_paquete)
        
    for id_camion, lista_paquetes in entregas_por_camion.items():
        print(f"\nCamión: {id_camion}")
        if lista_paquetes:
            print(f"  -> Paquetes asignados: {', '.join(lista_paquetes)}")
        else:
            print("  -> Sin paquetes asignados")

if __name__ == "__main__":
    main()