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
    print("Prueba de validación")

    camiones = [
        {"id": "C1", "capacidad": 20},
        {"id": "C2", "capacidad": 15}
    ]

    paquetes = [
        {"id": "P1", "peso": 10},
        {"id": "P2", "peso": 5},
        {"id": "P3", "peso": 8},
        {"id": "P4", "peso": 12}
    ]

    asignacion_valida = {
        "P1": "C2",
        "P2": "C2",
        "P3": "C1",
        "P4": "C1"
    }

    asignacion_invalida = {
        "P1": "C1",
        "P2": "C1",
        "P3": "C1",
        "P4": "C1"
    }

    print("Asignación válida:", es_asignacion_valida(
        asignacion_valida, camiones, paquetes
    ))

    print("Asignación inválida:", es_asignacion_valida(
        asignacion_invalida, camiones, paquetes
    ))