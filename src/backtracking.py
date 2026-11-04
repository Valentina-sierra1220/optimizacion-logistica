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


        # Poda por capacidad restante
        peso_restante = sum(
        p["peso"] for p in paquetes[indice:]
                                                        )

        capacidad_restante = sum(
            camiones[i]["capacidad"] - cargas[i]
                for i in range(len(camiones))   )

        if peso_restante > capacidad_restante:
            return

        for i in range(indice, len(paquetes)):
            if not any(
                cargas[c] + paquetes[i]["peso"] <= camiones[c]["capacidad"]
                for c in range(len(camiones))
            ):
                return


        paquete = paquetes[indice]
        peso = paquete["peso"]


        #probar camiones
        for camion in range(len(camiones)):
            # Poda por simetría
            
          
            capacidad = camiones[camion]["capacidad"]
            nueva_carga = cargas[camion] + peso

            #poda por capacidad
            if nueva_carga > capacidad:
                continue

            # Poda por duración mínima del turno
            tiempo_base_camion = sum(
            paquetes[j]["tiempo_viaje"] + paquetes[j]["tiempo_entrega"]
                for j in range(indice)
            if asignacion[j] == camion)

            tiempo_base_camion += (
                paquete["tiempo_viaje"] + paquete["tiempo_entrega"])

            duracion_turno = (
                camiones[camion]["hora_fin"] - camiones[camion]["hora_inicio"])

            if tiempo_base_camion > duracion_turno:
                continue


                # Registrar decisión
            asignacion.append(camion)
            cargas[camion] = nueva_carga

            # Poda por factibilidad parcial de la ruta
            paquetes_parciales = [
                paquetes[j]
                for j in range(indice + 1)
                if asignacion[j] == camion
            ]

            if not existe_ruta_valida(
                paquetes_parciales,
                camiones[camion]
            ):
                asignacion.pop()
                cargas[camion] -= peso
                continue
      

            # Avanzar recursivamente
            asignar_paquete(indice + 1, asignacion, cargas)


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
    def explorar(hora_actual, tiempo_restante):
        nonlocal mejor_ruta, mejor_hora_finalizacion

        # Caso base: todos los paquetes tienen un lugar en la ruta
        if len(ruta_actual) == len(paquetes):
            if hora_actual < mejor_hora_finalizacion:
                mejor_hora_finalizacion = hora_actual
                mejor_ruta = ruta_actual.copy()
            return

        if hora_actual + tiempo_restante >= mejor_hora_finalizacion:
            return

        # Poda por ventanas de tiempo perdidas
        for j, paquete in enumerate(paquetes):
            if not visitados[j]:
                if hora_actual + paquete["tiempo_viaje"] > paquete["ventana_fin"]:
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
            # Poda por hora de finalización del turno
            if tiempo_final > camion["hora_fin"]:
                continue

            # Tomar la decisión
            visitados[i] = True
            ruta_actual.append(paquete)

            # Explorar la siguiente entrega
            explorar(tiempo_final,tiempo_restante - paquete["tiempo_viaje"] - paquete["tiempo_entrega"])

            # Retroceder
            ruta_actual.pop()
            visitados[i] = False


    tiempo_restante = sum(
    p["tiempo_viaje"] + p["tiempo_entrega"]
    for p in paquetes)

    explorar(camion["hora_inicio"], tiempo_restante)

    return mejor_ruta, mejor_hora_finalizacion






def existe_ruta_valida(paquetes, camion):

    ruta_actual = []
    visitados = [False] * len(paquetes)

    def explorar(hora_actual):

        # Caso base: encontramos una ruta completa
        if len(ruta_actual) == len(paquetes):
            return True

        # Poda por ventanas de tiempo perdidas
        for j, paquete in enumerate(paquetes):
            if not visitados[j]:
                if hora_actual + paquete["tiempo_viaje"] > paquete["ventana_fin"]:
                    return False

        # Explorar las posibles entregas
        for i, paquete in enumerate(paquetes):

            if visitados[i]:
                continue

            tiempo_llegada = hora_actual + paquete["tiempo_viaje"]

            if tiempo_llegada < paquete["ventana_inicio"]:
                tiempo_llegada = paquete["ventana_inicio"]

            if tiempo_llegada > paquete["ventana_fin"]:
                continue

            tiempo_final = tiempo_llegada + paquete["tiempo_entrega"]

            if tiempo_final > camion["hora_fin"]:
                continue

            # Tomar decisión
            visitados[i] = True
            ruta_actual.append(paquete)

            # Explorar
            if explorar(tiempo_final):
                return True

            # Retroceder
            ruta_actual.pop()
            visitados[i] = False

        return False

    return explorar(camion["hora_inicio"])
