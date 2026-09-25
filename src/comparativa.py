import os
import sys
import time
import matplotlib.pyplot as plt
from fuerza_bruta import fuerza_bruta, cargar_casos


def ejecutar_comparativa():
    casos = [
        ("pequeño", "datos/caso_pequeno.txt"),
        ("mediano", "datos/caso_mediano.txt"),
        ("grande", "datos/caso_grande.txt")
    ]
    cantidades_paquetes = []  
    tiempos = []

    print("Iniciando medición empírica de tiempos de ejecución...")

    for nombre, ruta in casos:
        camiones, paquetes = cargar_casos(ruta)
        
        # Ocultar los print de fuerza_bruta para que la consola no colapse con n=12
        sys.stdout = open(os.devnull, 'w')

        # Medición de tiempo
        inicio = time.perf_counter()
        _, total = fuerza_bruta(paquetes, camiones)  # Se ejecuta la función directamente sin asignación
        fin = time.perf_counter()

        # Restaurar la salida normal de la terminal
        sys.stdout = sys.__stdout__

        tiempo_ejecucion = fin - inicio
        
        cantidades_paquetes.append(len(paquetes))
        tiempos.append(tiempo_ejecucion)

        print( f"{nombre}: " f"Paquetes={len(paquetes)} | " f"Combinaciones={total} | " f"Tiempo={tiempo_ejecucion:.6f}s" )
        

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

    print(f"\nAnálisis completado exitosamente. Gráfica guardada en '{ruta_grafica}'.")

if __name__ == "__main__":
    ejecutar_comparativa()