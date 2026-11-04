import os, sys, time, multiprocessing, matplotlib.pyplot as plt
from fuerza_bruta import fuerza_bruta, cargar_casos
from greedy import algoritmo_greedy
from divide_y_venceras import algoritmo_divide_y_venceras
from programacion_dinamica import asignar_paquetes_dp
from backtracking import asignar_paquetes_backtracking

# Función auxiliar para ejecutar con límite de tiempo
def ejecutar_con_timeout(func, args, limite_segundos=60.0):
    # Envolvemos la función para que se ejecute en un proceso separado
    p = multiprocessing.Process(target=func, args=args)
    t0 = time.perf_counter()
    p.start()
    p.join(limite_segundos) # Esperar máximo el límite de tiempo
    
    if p.is_alive():
        # Si sigue vivo después de 60s, lo matamos y retornamos el límite
        p.terminate()
        p.join()
        return limite_segundos
    else:
        # Si terminó antes, retornamos el tiempo real
        return time.perf_counter() - t0

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
    paquetes_n_dp, t_dp = [], []       
    paquetes_n_bt, t_bt = [], []

    print("Iniciando mediciones empíricas de tiempo...")

    for nombre, ruta in casos:
        camiones, paquetes = cargar_casos(ruta)
        n = len(paquetes)

        # 1. Medición Greedy 
        paquetes_n_greedy.append(n)
        old_stdout = sys.stdout  # Guardar salida original
        sys.stdout = open(os.devnull, 'w')
        t0 = time.perf_counter()
        algoritmo_greedy(paquetes, camiones)
        t_greedy.append(time.perf_counter() - t0)
        sys.stdout = old_stdout  # Restaurar salida de forma segura

        # 2. Medición Divide y Vencerás
        paquetes_n_dyv.append(n)
        t0 = time.perf_counter()
        algoritmo_divide_y_venceras(paquetes, camiones)
        t_dyv.append(time.perf_counter() - t0)

        # 3. Medición Fuerza Bruta 
        if n <= 16:
            paquetes_n_fb.append(n)
            t0 = time.perf_counter()
            fuerza_bruta(paquetes, camiones)
            t_fb.append(time.perf_counter() - t0)
            fb_str = f"{t_fb[-1]:.6f}s"
        else:
            fb_str = f"Omitido (Inviable)"

        # 4.  Medición Backtracking
        paquetes_n_bt.append(n)
        t_backtracking = ejecutar_con_timeout(asignar_paquetes_backtracking, (paquetes, camiones), 60.0)
        t_bt.append(t_backtracking)

        # 5.  Medición DP
        paquetes_n_dp.append(n)
        t_dinamica = ejecutar_con_timeout(asignar_paquetes_dp, (paquetes, camiones), 60.0)
        t_dp.append(t_dinamica)
        
        # AHORA SÍ IMPRIMIMOS TODO (Incluyendo FB, Backtracking y DP)
        print(f"[{nombre.upper()}] Paquetes={n} | Greedy={t_greedy[-1]:.6f}s | D&V={t_dyv[-1]:.6f}s | FB={fb_str} | BT={t_bt[-1]:.6f}s | DP={t_dp[-1]:.6f}s")


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

    # ==========================================
    # --- NUEVA GRÁFICA 4: BACKTRACKING ---
    # ==========================================
    plt.figure(figsize=(9, 5))
    plt.plot(paquetes_n_bt, t_bt, 'r-o', linewidth=2, label='Backtracking (Con Podas)')
    # Dibujar línea roja punteada indicando el Timeout
    plt.axhline(y=60, color='r', linestyle=':', label='Timeout (60s)')
    plt.title('Análisis Empírico de Tiempos - Backtracking', fontweight='bold', fontsize=12)
    plt.xlabel('Número de Paquetes (n)', fontsize=10)
    plt.ylabel('Tiempo de Ejecución (segundos)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    ruta_bt = "src/grafica_backtracking_logistica.png"
    plt.savefig(ruta_bt, dpi=300, bbox_inches='tight')
    plt.close()


    # ==========================================
    # --- NUEVA GRÁFICA 5: PROGRAMACIÓN DINÁMICA ---
    # ==========================================
    plt.figure(figsize=(9, 5))
    plt.plot(paquetes_n_dp, t_dp, 'c-o', linewidth=2, label='DP (Top-Down Memoization)')
    # Dibujar línea roja punteada indicando el Timeout
    plt.axhline(y=60, color='r', linestyle=':', label='Timeout (60s)')
    plt.title('Análisis Empírico de Tiempos - Programación Dinámica', fontweight='bold', fontsize=12)
    plt.xlabel('Número de Paquetes (n)', fontsize=10)
    plt.ylabel('Tiempo de Ejecución (segundos)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    ruta_dp = "src/grafica_dp_logistica.png"
    plt.savefig(ruta_dp, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\n¡Gráficas independientes guardadas con éxito!\n{ruta_fb}\n{ruta_greedy}\n{ruta_dyv}\n{ruta_bt}\n{ruta_dp}")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    ejecutar_comparativa()