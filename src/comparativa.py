"""
MÓDULO DE ANÁLISIS EMPÍRICO Y COMPARATIVA DE TIEMPOS
===================================================
Mide el tiempo real de ejecución de la Fuerza Bruta O(m^n) 
y genera la gráfica en la carpeta `src/`.
"""

import json
import time
import matplotlib.pyplot as plt
from fuerza_bruta import resolver_fuerza_bruta  # Importación directa

def crear_caso_sintetico(n_paquetes: int, m_camiones: int = 2) -> str:
    """Crea un archivo JSON de prueba con n paquetes y m camiones."""
    datos = {
        "camiones": [{"id": f"C{i+1}", "capacidad": 30} for i in range(m_camiones)],
        "paquetes": [{"id": f"P{i+1}", "peso": 5} for i in range(n_paquetes)]
    }
    ruta = "datos/caso_temp_comparativa.txt"
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2)
    return ruta

def ejecutar_analisis_empirico():
    """Ejecuta las pruebas, mide tiempos reales y genera la gráfica."""
    casos_n = [2, 4, 6, 8, 10, 12]
    tiempos = []

    print("\n--- MEDIENDO TIEMPOS REALES (FUERZA BRUTA) ---")
    for n in casos_n:
        ruta = crear_caso_sintetico(n_paquetes=n)
        
        # Medición de tiempo exacto
        inicio = time.perf_counter()
        _, total_evaluadas = resolver_fuerza_bruta(ruta)
        duracion = time.perf_counter() - inicio
        
        tiempos.append(duracion)
        print(f"Paquetes (n): {n:2d} | Combinaciones: {total_evaluadas:6d} | Tiempo: {duracion:.6f}s")

    # Generación de gráfica
    plt.figure(figsize=(7, 4.5))
    plt.plot(casos_n, tiempos, 'o-', color='#1f77b4', linewidth=2, label='Fuerza Bruta $O(m^n)$')
    plt.title('Tiempo de Ejecución vs. Cantidad de Paquetes', fontweight='bold')
    plt.xlabel('Número de Paquetes ($n$)')
    plt.ylabel('Tiempo (Segundos)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    
    # Guardar en src/
    plt.savefig('src/grafica_fuerza_bruta_logistica.png', dpi=300)
    print("\n Gráfica guardada en 'src/grafica_fuerza_bruta_logistica.png'\n")

if __name__ == '__main__':
    ejecutar_analisis_empirico()