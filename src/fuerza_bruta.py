import json

def es_asignacion_valida(asignacion, camiones, paquetes):
    for camion in camiones:
        peso_total = 0
        for paquete in paquetes:
            if asignacion[paquete["id"]] == camion["id"]:
                peso_total += paquete["peso"]
        if peso_total > camion["capacidad"]:
            return False

    return True
def fuerza_bruta(paquetes,camiones):
    soluciones= []
    total_evaluadas = 0
    
    def generar_asignaciones(indice, asignacion):
        nonlocal total_evaluadas

        if indice == len(paquetes):
            total_evaluadas += 1
            if es_asignacion_valida(asignacion,camiones,paquetes):
                soluciones.append(asignacion)
            return

        paquete = paquetes[indice]
        for camion in camiones:
            nueva_asignacion = asignacion.copy()
            nueva_asignacion[paquete["id"]] = camion["id"]
            generar_asignaciones(indice + 1,nueva_asignacion )

    generar_asignaciones(0,{})
    return soluciones, total_evaluadas



def cargar_casos(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

        return datos["camiones"], datos["paquetes"]



if __name__ == "__main__":
    camiones, paquetes = cargar_casos("datos/caso_pequeno.txt")

    soluciones, total_evaluadas =fuerza_bruta(paquetes, camiones)
    print("soluciones encontradas", soluciones, total_evaluadas)