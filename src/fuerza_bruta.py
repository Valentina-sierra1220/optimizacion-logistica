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
    soluciones= []   #O(1)
    total_evaluadas = 0   #O(1)
    
    def generar_asignaciones(indice, asignacion): #O(1)
        nonlocal total_evaluadas  #O(1)

        if indice == len(paquetes):  #O(1)
            total_evaluadas += 1 #O(1)
            if es_asignacion_valida(asignacion,camiones,paquetes):  #(m*n)
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
    camiones, paquetes = cargar_casos("datos/caso_pequeno.txt")

    soluciones, total_evaluadas =fuerza_bruta(paquetes, camiones)
    print("soluciones encontradas", soluciones, total_evaluadas)