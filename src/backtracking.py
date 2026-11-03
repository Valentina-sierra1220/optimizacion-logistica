def backtracking(paquetes, camiones):

    asignacion = []
    cargas = [0] * len(camiones)
    mejor_solucion = None
    mejor_tiempo_finalizacion = float("inf")


    def asignar_paquete(indice, asignacion, cargas):
        nonlocal mejor_solucion,mejor_tiempo_finalizacion

        #caso base
                
        if indice == len(paquetes):

            paquetes_por_camion = [[] for _ in camiones]

            for i, camion in enumerate(asignacion):
                paquetes_por_camion[camion].append(paquetes[i])

            tiempos = []

            for i in range(len(camiones)):
                ruta, hora = buscar_mejor_ruta(
                    paquetes_por_camion[i], camiones[i]
                )

                if ruta is None:
                    return

                tiempos.append(hora)

            tiempo_total = max(tiempos)

            if tiempo_total < mejor_tiempo_finalizacion:
                mejor_tiempo_finalizacion = tiempo_total
                mejor_solucion = asignacion.copy()

            return


        paquete = paquetes[indice]
        peso = paquete["peso"]


        #probar camiones
        for camion in range(len(camiones)):
            # Poda por simetría
            
            equivalentes = [
                i for i in range(camion)
                if camiones[i]["capacidad"] == camiones[camion]["capacidad"]
                and camiones[i]["hora_inicio"] == camiones[camion]["hora_inicio"]
                and cargas[i] == cargas[camion]
            ]

            if equivalentes:
                continue
            capacidad = camiones[camion]["capacidad"]
            nueva_carga = cargas[camion] + peso

            #poda por capacidad
            if nueva_carga > capacidad:
                continue

            #registrar decison
            asignacion.append(camion)
            cargas[camion] = nueva_carga

             #avanzamos recursivamente
            asignar_paquete(indice +1, asignacion, cargas)


            #retrocedemos
            asignacion.pop()
            cargas[camion] -= peso


    asignar_paquete(0, asignacion, cargas)

    return mejor_solucion



def buscar_mejor_ruta(paquetes, camion):
    ruta_actual = []
    visitados = [False] * len(paquetes)

    mejor_ruta = None
    mejor_hora_finalizacion = float("inf")
    def explorar(hora_actual):
        nonlocal mejor_ruta, mejor_hora_finalizacion

        # Caso base: todos los paquetes tienen un lugar en la ruta
        if len(ruta_actual) == len(paquetes):
            if hora_actual < mejor_hora_finalizacion:
                mejor_hora_finalizacion = hora_actual
                mejor_ruta = ruta_actual.copy()
            return

        tiempo_restante = sum(
            p["tiempo_viaje"] + p["tiempo_entrega"]
            for i, p in enumerate(paquetes)
            if not visitados[i]
        )

        if hora_actual + tiempo_restante >= mejor_hora_finalizacion:
            return

        for i, paquete in enumerate(paquetes):

            if visitados[i]:
                continue

            tiempo_llegada = hora_actual + paquete["tiempo_viaje"]

            if tiempo_llegada < paquete["ventana_inicio"]:
                tiempo_llegada = paquete["ventana_inicio"]

            if tiempo_llegada > paquete["ventana_fin"]:
                continue

            tiempo_final = tiempo_llegada + paquete["tiempo_entrega"]

            # Tomar la decisión
            visitados[i] = True
            ruta_actual.append(paquete)

            # Explorar la siguiente entrega
            explorar(tiempo_final)

            # Retroceder
            ruta_actual.pop()
            visitados[i] = False


    explorar(camion["hora_inicio"])

    return mejor_ruta, mejor_hora_finalizacion