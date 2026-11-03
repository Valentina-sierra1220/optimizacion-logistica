import os, sys, time, matplotlib.pyplot as plt
from fuerza_bruta import fuerza_bruta, cargar_casos
from greedy import algoritmo_greedy
from divide_y_venceras import algoritmo_divide_y_venceras

def ejecutar_comparativa():
    casos = [
        ("pequeño", "datos/caso_pequeno.txt"), 
        ("mediano", "datos/caso_mediano.txt"), 
        ("grande", "datos/caso_grande.txt"),
        ("estrés", "datos/caso_estres.txt")
    ]
    
    paquetes_n_fb, t_fb = [], []
    paquetes_n_greedy, t_greedy = [], []
    paquetes_n_dyv, t_dyv = [], []

    print("Iniciando mediciones empíricas de tiempo (Greedy, Fuerza Bruta y Divide y Vencerás)...")

    for nombre, ruta in casos:
        camiones, paquetes = cargar_casos(ruta)
        n = len(paquetes)

        # 1. Medición Greedy (Aplica para todos los casos)
        paquetes_n_greedy.append(n)
        sys.stdout = open(os.devnull, 'w')
        t0 = time.perf_counter()
        algoritmo_greedy(paquetes, camiones)
        t_greedy.append(time.perf_counter() - t0)
        sys.stdout = sys.__stdout__

        # 2. Medición Divide y Vencerás (Aplica para todos los casos)
        paquetes_n_dyv.append(n)
        t0 = time.perf_counter()
        algoritmo_divide_y_venceras(paquetes, camiones)
        t_dyv.append(time.perf_counter() - t0)

        # 3. Medición Fuerza Bruta (Solo hasta n <= 16 por viabilidad exponencial)
        if n <= 16:
            paquetes_n_fb.append(n)
            t0 = time.perf_counter()
            fuerza_bruta(paquetes, camiones)
            t_fb.append(time.perf_counter() - t0)
            print(f"[{nombre.upper()}] Paquetes={n} | Greedy={t_greedy[-1]:.6f}s | D&V={t_dyv[-1]:.6f}s | Fuerza Bruta={t_fb[-1]:.6f}s")
        else:
            print(f"[{nombre.upper()}] Paquetes={n} | Greedy={t_greedy[-1]:.6f}s | D&V={t_dyv[-1]:.6f}s | Fuerza Bruta=Omitido (Inviable para n={n})")

    os.makedirs("src", exist_ok=True)

    # ==========================================
    # --- GRÁFICA 1: Fuerza Bruta ---
    # ==========================================
    plt.figure(figsize=(9, 5))
    plt.plot(paquetes_n_fb, t_fb, 'b-o', linewidth=2, label='Fuerza Bruta O(m^n)')
    plt.title('Análisis Empírico de Tiempos de Ejecución - Fuerza Bruta', fontweight='bold', fontsize=12)
    plt.xlabel('Número de Paquetes (n)', fontsize=10)
    plt.ylabel('Tiempo de Ejecución (segundos)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    ruta_fb = "src/grafica_fuerza_bruta_logistica.png"
    plt.savefig(ruta_fb, dpi=300, bbox_inches='tight')
    plt.close()

    # ==========================================
    # --- GRÁFICA 2: Greedy ---
    # ==========================================
    plt.figure(figsize=(9, 5))
    plt.plot(paquetes_n_greedy, t_greedy, 'g-o', linewidth=2, label='Greedy O(n log n)')
    plt.title('Análisis Empírico de Tiempos de Ejecución - Algoritmo Greedy', fontweight='bold', fontsize=12)
    plt.xlabel('Número de Paquetes (n)', fontsize=10)
    plt.ylabel('Tiempo de Ejecución (segundos)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    ruta_greedy = "src/grafica_greedy_logistica.png"
    plt.savefig(ruta_greedy, dpi=300, bbox_inches='tight')
    plt.close()

    # ==========================================
    # --- GRÁFICA 3: Divide y Vencerás ---
    # ==========================================
    plt.figure(figsize=(9, 5))
    plt.plot(paquetes_n_dyv, t_dyv, 'm-o', linewidth=2, label='Divide y Vencerás O(n)')
    plt.title('Análisis Empírico de Tiempos de Ejecución - Divide y Vencerás', fontweight='bold', fontsize=12)
    plt.xlabel('Número de Paquetes (n)', fontsize=10)
    plt.ylabel('Tiempo de Ejecución (segundos)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    ruta_dyv = "src/grafica_divide_y_venceras_logistica.png"
    plt.savefig(ruta_dyv, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\n¡Gráficas independientes guardadas con éxito!\n - {ruta_fb}\n - {ruta_greedy}\n - {ruta_dyv}")

if __name__ == "__main__":
    ejecutar_comparativa()