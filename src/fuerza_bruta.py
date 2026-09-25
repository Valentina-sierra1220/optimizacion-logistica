import json
import time

def es_asignacion_valida(asignacion, camiones, paquetes):
    for camion in camiones:
        peso_total = 0
        for paquete in paquetes:
            if asignacion[paquete["id"]] == camion["id"]:
                peso_total += paquete["peso"]
        if peso_total > camion["capacidad"]:
            return False

    return True


def validar_orden_entrega(orden, paquetes, camion):
    tiempo_actual = camion["hora_inicio"] #O(1)
    for paquete in orden: #O(n)
        for p in paquetes: #O(n)
            if p["id"] == paquete["id"]:
                datos_paquete = p
                break

        tiempo_llegada = tiempo_actual + datos_paquete["tiempo_viaje"]

        if tiempo_llegada < datos_paquete["ventana_inicio"]:
            tiempo_llegada = datos_paquete["ventana_inicio"]

        if tiempo_llegada > datos_paquete["ventana_fin"]:
            return False

        tiempo_actual = tiempo_llegada + datos_paquete["tiempo_entrega"]
    return True

def generar_ordenes(paquetes, camion):
    ordenes_validas = []
    def generar(actual, restantes):
        if not restantes:
            if validar_orden_entrega(actual, paquetes, camion):
                ordenes_validas.append(actual)
            return

        for paquete in restantes:
            nuevo_actual = actual + [paquete]
            nuevos_restantes = [p for p in restantes if p != paquete]
            generar(nuevo_actual, nuevos_restantes)

    generar([], paquetes)
    return ordenes_validas

 
def fuerza_bruta(paquetes,camiones):
    soluciones= []   #O(1)
    total_evaluadas = 0   #O(1)
    
    def generar_asignaciones(indice, asignacion): #O(1)
        nonlocal total_evaluadas  #O(1)

        if indice == len(paquetes):  #O(1)
            total_evaluadas += 1 #O(1)
            if es_asignacion_valida(asignacion,camiones,paquetes):  #(m*n)
                asignacion_valida = True
                for camion in camiones:
                    paquetes_camion = []

                    for paquete in paquetes:
                        if asignacion[paquete["id"]] == camion["id"]:
                            paquetes_camion.append(paquete)
                    ordenes = generar_ordenes(paquetes_camion, camion)
                    
                    if not ordenes:
                        asignacion_valida = False
                        break

                if asignacion_valida:
                    soluciones.append(asignacion) #O(1)*

            return #O(1)

        paquete = paquetes[indice] #O(1)
        for camion in camiones: #O(m)
            nueva_asignacion = asignacion.copy() #O(n)
            nueva_asignacion[paquete["id"]] = camion["id"] #O(1)*
            generar_asignaciones(indice + 1,nueva_asignacion ) # Genera el árbol de posibilidades
            #Número total de asignaciones generadas = m^n

    generar_asignaciones(0,{}) #0(1) inicial
    return soluciones, total_evaluadas #0(1)








def cargar_casos(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

        return datos["camiones"], datos["paquetes"]



if __name__ == "__main__":
    print("Prueba de fuerza bruta")

    camiones, paquetes = cargar_casos("datos/caso_pequeno.txt")
    inicio = time.time()
    soluciones, total = fuerza_bruta(paquetes, camiones)
    fin = time.time()
    print("Asignaciones evaluadas:", total)
    print("Soluciones encontradas:", len(soluciones))
    print("Tiempo de ejecución:", fin - inicio, "segundos")
    