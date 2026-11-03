import json
from pathlib import Path
from src.backtracking import backtracking, buscar_mejor_ruta
import time

# Cargar caso de prueba
ruta_archivo = Path("datos/caso_grande.txt")

with open(ruta_archivo, "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

paquetes = datos["paquetes"]
camiones = datos["camiones"]

# Ejecutar Backtracking completo
inicio = time.perf_counter()

resultado = backtracking(paquetes, camiones)

fin = time.perf_counter()

tiempo_ejecucion = fin - inicio

if resultado is None:
    print("No se encontró una solución válida.")

else:
    print("\n========== RESULTADO BACKTRACKING ==========")

    print("\nAsignación:", resultado)
    print(f"Tiempo de ejecución: {tiempo_ejecucion:.8f} segundos")

    tiempos = []

    for i, camion in enumerate(camiones):

        paquetes_camion = [
            paquetes[j]
            for j, asignado in enumerate(resultado)
            if asignado == i
        ]

        ruta, hora = buscar_mejor_ruta(paquetes_camion, camion)

        print(f"\nCamión {camion['id']}")
        print("Carga:", sum(p["peso"] for p in paquetes_camion))
        print("Capacidad:", camion["capacidad"])
        print("Ruta:", [p["id"] for p in ruta])
        print("Hora final:", hora)

        tiempos.append(hora)

    print("\nTiempo de finalización total:", max(tiempos))