def backtracking(paquetes, camiones):

    asignacion = []
    cargas = [0] * len(camiones)

    def asignar_paquete(indice, asignacion, cargas):
        if indice == len(paquetes):
            return True

        paquete = paquetes[indice]
        peso = paquete["peso"]
        
        for camion in range(len(camiones)):
            capacidad = camiones[camion]["capacidad"]
            nueva_carga = cargas[camion] + peso

            print(f"Probando paquete {indice} en camión {camion}")

    asignar_paquete(0, asignacion, cargas)

    return asignacion