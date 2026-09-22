import json

# ==========================================
# 1. FUNCIÓN PARA CARGAR LOS DATOS DEL JSON
# ==========================================
def cargar_caso_prueba(ruta_archivo):
    """
    Abre el archivo JSON y extrae las listas de camiones y paquetes.
    """
    # Abre el archivo especificado en la ruta (modo lectura)
    with open(ruta_archivo, 'r') as archivo:
        datos = json.load(archivo)  # Convierte el archivo JSON en un diccionario de Python
    
    # Devuelve la lista de camiones y la lista de paquetes por separado
    return datos["camiones"], datos["paquetes"]


# ==========================================
# 2. FUNCIÓN PARA VALIDAR LA ASIGNACIÓN
# ==========================================
def es_asignacion_valida(asignacion, camiones, paquetes):
    """
    Revisa si la asignación propuesta supera la capacidad de algún camión.
    
    :param asignacion: Diccionario de ejemplo {"P1": "C1", "P2": "C2"}
    :param camiones: Lista de camiones con sus capacidades
    :param paquetes: Lista de paquetes con sus pesos
    """
    # Recorremos la lista de camiones uno por uno
    for camion in camiones:
        peso_total = 0  # Guardará la suma del peso de los paquetes en este camión
        
        # Recorremos la lista de paquetes para buscar cuáles van a este camión
        for paquete in paquetes:
            # Si el paquete actual está asignado al camión que estamos revisando
            if asignacion[paquete["id"]] == camion["id"]:
                peso_total += paquete["peso"]  # Sumamos el peso del paquete
        
        # Si la suma de pesos supera la capacidad máxima del camión
        if peso_total > camion["capacidad"]:
            return False  # La combinación NO es válida, se rechaza de inmediato
            
    # Si revisamos todos los camiones y ninguno se sobrecargó, la combinación SÍ es válida
    return True


# ==========================================
# 3. BLOQUE DE PRUEBA LOCAL
# ==========================================
if __name__ == '__main__':
    print("--- PROBANDO LAS FUNCIONES AUXILIARES ---\n")
    
    # 1. Cargamos los datos del caso pequeño (usamos ../datos/ porque estamos dentro de src/)
    camiones, paquetes = cargar_caso_prueba('../datos/caso_pequeno.json')
    
    print("Camiones cargados:", camiones)
    print("Paquetes cargados:", paquetes)
    print("-" * 40)

    # 2. Creamos una prueba donde SÍ caben los paquetes:
    # C1 (capacidad 20): P1(10) + P2(5) = 15 <= 20 (Válido)
    # C2 (capacidad 15): P3(8) = 8 <= 15 (Válido)
    # (Nota: P4 no asignado en esta prueba simple para demostración)
    asignacion_correcta = {"P1": "C1", "P2": "C1", "P3": "C2", "P4": "C2"}

    # 3. Creamos una prueba donde NO caben los paquetes:
    # C1 (capacidad 20): P1(10) + P4(12) = 22 > 20 (Sobrecargado)
    asignacion_incorrecta = {"P1": "C1", "P2": "C2", "P3": "C2", "P4": "C1"}

    # 4. Probamos la función con ambos ejemplos
    print("Prueba 1 (Asignación Válida):", es_asignacion_valida(asignacion_correcta, camiones, paquetes))
    print("Prueba 2 (Asignación Inválida):", es_asignacion_valida(asignacion_incorrecta, camiones, paquetes))