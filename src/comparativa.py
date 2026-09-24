import os
import sys
import time
import matplotlib.pyplot as plt
from fuerza_bruta import fuerza_bruta

def generar_caso_temporal(num_paquetes, num_camiones=2, capacidad_camion=30):
    """Crea las listas de camiones y paquetes para n paquetes."""
    camiones = [{"id": f"C{i+1}", "capacidad": capacidad_camion} for i in range(num_camiones)]
    paquetes = [{"id": f"P{i+1}", "peso": (i % 5) + 3} for i in range(num_paquetes)]
    return camiones, paquetes

def ejecutar_comparativa():
    cantidades_paquetes = range(2, 13)  # n de 2 a 12
    tiempos = []

    print("Iniciando medición empírica de tiempos de ejecución...")

    for n in cantidades_paquetes:
        camiones, paquetes = generar_caso_temporal(n)
        
        # Ocultar los print de fuerza_bruta para que la consola no colapse con n=12
        sys.stdout = open(os.devnull, 'w')

        # Medición de tiempo
        inicio = time.perf_counter()
        _, total = fuerza_bruta(paquetes, camiones)  # Se ejecuta la función directamente sin asignación
        fin = time.perf_counter()

        # Restaurar la salida normal de la terminal
        sys.stdout = sys.__stdout__

        tiempo_ejecucion = fin - inicio
        
        
        tiempos.append(tiempo_ejecucion)

        print(f"Paquetes (n={n}): Combinaciones={total} | Tiempo={tiempo_ejecucion:.6f}s")

    # Generar y guardar la gráfica en la carpeta src/
    plt.figure(figsize=(9, 5))
    plt.plot(list(cantidades_paquetes), tiempos, marker='o', color='b', linestyle='-', linewidth=2, label='Fuerza Bruta O(m^n)')
    
    plt.title('Análisis Empírico de Tiempos de Ejecución - Fuerza Bruta', fontsize=12, fontweight='bold')
    plt.xlabel('Número de Paquetes (n)', fontsize=10)
    plt.ylabel('Tiempo de Ejecución (segundos)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    ruta_grafica = "src/grafica_fuerza_bruta_logistica.png"
    os.makedirs("src", exist_ok=True)
    plt.savefig(ruta_grafica, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\n✅ Análisis completado exitosamente. Gráfica guardada en '{ruta_grafica}'.")

if __name__ == "__main__":
    ejecutar_comparativa()