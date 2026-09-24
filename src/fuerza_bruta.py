def fuerza_bruta(paquetes,camiones):
    
    def generar_asignaciones(indice, asignacion):

        if indice == len(paquetes):
            print("asigancion completa", asignacion)
            return

        paquete = paquetes[indice]
        print("estoy procesando: ", paquete["id"])
        for camion in camiones:
            print(paquete["id"],"->", camion["id"])
            nueva_asignacion = asignacion.copy()
            nueva_asignacion[paquete["id"]] = camion["id"]
            generar_asignaciones(indice + 1,nueva_asignacion )

    generar_asignaciones(0,{})



   


if __name__ == "__main__":
    print("Prueba de fuerza bruta")
    camiones, paquetes = cargar_caso_prueba("datos/caso_pequeno.txt")
    fuerza_bruta(paquetes, camiones)