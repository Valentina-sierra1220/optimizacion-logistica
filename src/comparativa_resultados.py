
import time
import multiprocessing

from fuerza_bruta import fuerza_bruta, cargar_casos
from greedy import algoritmo_greedy
from divide_y_venceras import algoritmo_divide_y_venceras
from programacion_dinamica import asignar_paquetes_dp
from backtracking import asignar_paquetes_backtracking


# =====================================================
# EJECUTAR ALGORITMO EN UN PROCESO SEPARADO
# =====================================================

def trabajador(func, args, conexion):

    import time
    import io
    import contextlib

    inicio = time.perf_counter()
    salida = io.StringIO()

    try:

        with contextlib.redirect_stdout(salida):
            resultado = func(*args)

        tiempo = time.perf_counter() - inicio

        conexion.send(("ok", resultado, tiempo))

    except Exception as e:

        tiempo = time.perf_counter() - inicio

        conexion.send(("error", str(e), tiempo))

    finally:
        conexion.close()


# =====================================================
# CONTROLAR TIEMPO DE EJECUCIÓN
# =====================================================

def ejecutar_algoritmo(func, args, limite=60):

    receptor, emisor = multiprocessing.Pipe(duplex=False)

    proceso = multiprocessing.Process(
        target=trabajador,
        args=(func, args, emisor)
    )

    proceso.start()
    emisor.close()

    proceso.join(limite)

    if proceso.is_alive():

        proceso.terminate()
        proceso.join()
        receptor.close()

        return None, limite, "TIMEOUT"

    if receptor.poll():

        estado, resultado, tiempo = receptor.recv()
        receptor.close()

        if estado == "error":
            return None, tiempo, f"ERROR: {resultado}"

        return resultado, tiempo, "OK"

    receptor.close()

    return None, 0, "ERROR: El proceso terminó sin devolver resultados."


# =====================================================
# AGRUPAR PAQUETES POR CAMIÓN
# =====================================================

def agrupar_asignaciones(nombre, resultado):

    asignaciones = {}

    # -------------------------------------------------
    # FUERZA BRUTA
    # -------------------------------------------------

    if nombre == "FUERZA BRUTA":

        soluciones, total = resultado

        if not soluciones:
            return {}, "No se encontraron soluciones."

        # Mostrar solamente la primera solución.

        solucion = soluciones[0]

        if isinstance(solucion, dict):

            if "asignaciones" in solucion:
                solucion = solucion["asignaciones"]

            else:
                # Diccionario de tipo camion -> paquetes
                for camion, paquetes in solucion.items():

                    if isinstance(paquetes, list):
                        asignaciones[camion] = paquetes

                    else:
                        asignaciones[camion] = [paquetes]

                return asignaciones, None

        if isinstance(solucion, list):

            for item in solucion:

                if isinstance(item, dict):

                    camion = item.get(
                        "camion",
                        item.get("camion_id")
                    )

                    paquetes = item.get(
                        "paquetes",
                        item.get("paquetes_asignados", [])
                    )

                    if camion is not None:

                        if not isinstance(paquetes, list):
                            paquetes = [paquetes]

                        asignaciones.setdefault(camion, []).extend(paquetes)

                elif isinstance(item, (tuple, list)) and len(item) == 2:

                    paquete, camion = item

                    asignaciones.setdefault(camion, []).append(paquete)

        return asignaciones, None

    # -------------------------------------------------
    # GREEDY
    # -------------------------------------------------

    elif nombre == "GREEDY":

        asignacion, total = resultado

        for paquete, camion in asignacion.items():

            asignaciones.setdefault(camion, []).append(paquete)

        return asignaciones, None

    # -------------------------------------------------
    # BACKTRACKING Y PROGRAMACIÓN DINÁMICA
    # -------------------------------------------------

    elif nombre in ("BACKTRACKING", "PROGRAMACIÓN DINÁMICA"):

        cantidad, lista_asignaciones = resultado

        for paquete, camion in lista_asignaciones:

            asignaciones.setdefault(camion, []).append(paquete)

        return asignaciones, None

    # -------------------------------------------------
    # DIVIDE Y VENCERÁS
    # -------------------------------------------------

    elif nombre == "DIVIDE Y VENCERÁS":

        informacion, lista_paquetes = resultado

        # Este método actualmente no devuelve
        # una relación paquete-camión.

        return {}, (
            f"Factible: {informacion.get('factible')}\n"
            f"Paquetes procesados: {informacion.get('total_paquetes')}\n"
            f"Peso total: {informacion.get('peso_total')} kg\n"
            "El algoritmo no devuelve asignaciones por camión."
        )

    return {}, "Formato de resultado no reconocido."


# =====================================================
# IMPRIMIR ASIGNACIÓN FINAL
# =====================================================

def mostrar_asignaciones(nombre, resultado, paquetes, camiones):

    if resultado is None:

        print("No hay resultados disponibles.")
        return

    asignaciones, mensaje = agrupar_asignaciones(
        nombre,
        resultado
    )

    if mensaje:

        print("\n" + mensaje)

        if not asignaciones:
            return

    print("\nASIGNACIÓN FINAL DE PAQUETES")
    print("-" * 55)

    for camion in camiones:

        camion_id = camion["id"]
        capacidad = camion.get("capacidad", 0)

        paquetes_camion = asignaciones.get(camion_id, [])

        peso_total = 0

        print(f"\nCAMIÓN {camion_id}")
        print("-" * 45)

        if not paquetes_camion:

            print("Sin paquetes asignados.")
            continue

        for identificador in paquetes_camion:

            # Obtener ID si viene como diccionario.

            if isinstance(identificador, dict):

                identificador = identificador.get(
                    "id",
                    identificador.get("paquete")
                )

            paquete = next(
                (
                    p for p in paquetes
                    if str(p["id"]) == str(identificador)
                ),
                None
            )

            if paquete:

                peso = paquete.get("peso", 0)
                destino = paquete.get("destino", "Sin destino")

                peso_total += peso

                print(
                    f"{paquete['id']} | "
                    f"Destino: {destino} | "
                    f"Peso: {peso} kg"
                )

            else:

                print(f"Paquete {identificador}")

        print("-" * 45)

        print(f"Peso total transportado: {peso_total} kg")

        if capacidad:

            porcentaje = (peso_total / capacidad) * 100

            print(f"Capacidad del camión: {capacidad} kg")
            print(f"Ocupación: {porcentaje:.2f}%")


# =====================================================
# EJECUTAR TODOS LOS ALGORITMOS
# =====================================================

def ejecutar_resultados():

    casos = [

        ("PEQUEÑO", "datos/caso_pequeno.txt"),
        ("MEDIANO", "datos/caso_mediano.txt"),
        ("GRANDE", "datos/caso_grande.txt"),
        ("ESTRÉS", "datos/caso_estres.txt")

    ]

    algoritmos = [

        ("FUERZA BRUTA", fuerza_bruta),

        ("GREEDY", algoritmo_greedy),

        ("DIVIDE Y VENCERÁS", algoritmo_divide_y_venceras),

        ("BACKTRACKING", asignar_paquetes_backtracking),

        ("PROGRAMACIÓN DINÁMICA", asignar_paquetes_dp)

    ]

    print("\n")
    print("=" * 65)
    print("              RESULTADOS DE OPTIMIZACIÓN")
    print("=" * 65)

    # Recorrer cada instancia.

    for nombre_caso, ruta in casos:

        print("\n\n")
        print("#" * 65)
        print(f"                    CASO {nombre_caso}")
        print("#" * 65)

        camiones, paquetes = cargar_casos(ruta)

        print(f"\nNúmero de paquetes: {len(paquetes)}")
        print(f"Número de camiones: {len(camiones)}")

        tiempos = []

        # Ejecutar cada algoritmo.

        for nombre, algoritmo in algoritmos:

            print("\n\n")
            print("=" * 65)
            print(f"                    {nombre}")
            print("=" * 65)

            # Evitar ejecuciones inviables de fuerza bruta.

            if nombre == "FUERZA BRUTA" and len(paquetes) > 16:

                print("\nEjecución omitida: demasiados paquetes.")

                tiempos.append((nombre, "OMITIDO"))
                continue

            resultado, tiempo, estado = ejecutar_algoritmo(
                algoritmo,
                (paquetes, camiones),
                60
            )

            # Comprobar tiempo límite.

            if estado == "TIMEOUT":

                print("\nEl algoritmo superó el límite de 60 segundos.")

                tiempos.append((nombre, "TIMEOUT"))
                continue

            # Comprobar errores.

            if estado != "OK":

                print(f"\n{estado}")

                tiempos.append((nombre, "ERROR"))
                continue

            # Mostrar tiempo de ejecución.

            print(f"\nTiempo de ejecución: {tiempo:.6f} segundos")

            # Mostrar únicamente la asignación final.

            mostrar_asignaciones(
                nombre,
                resultado,
                paquetes,
                camiones
            )

            tiempos.append((nombre, tiempo))

        # -------------------------------------------------
        # RESUMEN DE TIEMPOS
        # -------------------------------------------------

        print("\n\n")
        print("-" * 65)
        print(f"             RESUMEN DE TIEMPOS - {nombre_caso}")
        print("-" * 65)

        print(f"{'ALGORITMO':<30} {'TIEMPO'}")
        print("-" * 65)

        for nombre, tiempo in tiempos:

            if isinstance(tiempo, (int, float)):

                print(
                    f"{nombre:<30} "
                    f"{tiempo:.6f} segundos"
                )

            else:

                print(f"{nombre:<30} {tiempo}")

    print("\n\n")
    print("=" * 65)
    print("                FIN DE LAS EJECUCIONES")
    print("=" * 65)


# =====================================================
# PROGRAMA PRINCIPAL
# =====================================================

if __name__ == "__main__":

    multiprocessing.freeze_support()

    ejecutar_resultados()
