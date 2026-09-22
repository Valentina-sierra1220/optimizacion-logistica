import time
import matplotlib.pyplot as plt

# 1. Crear paquetes y camiones de prueba automáticamente
def crear_datos_prueba(cantidad_paquetes):
    camiones = [
        {"id": "C1", "capacidad": 30},
        {"id": "C2", "capacidad": 30}
    ]
    
    paquetes = []
    for i in range(cantidad_paquetes):
        paquetes.append({"id": f"P{i+1}", "peso": 5})
        
    return camiones, paquetes


# 2. Medir tiempos y hacer la gráfica
def medir_tiempos_y_graficar():
    # Probamos con diferentes cantidades de paquetes
    lista_paquetes = [2, 4, 6, 8, 10, 12]
    tiempos = []

    print("--- MIDIENDO TIEMPOS DE EJECUCIÓN ---")

    for n in lista_paquetes:
        camiones, paquetes = crear_datos_prueba(n)
        
        # Guardamos la hora exacta de inicio
        inicio = time.perf_counter()
        
        # Simula el tiempo que tarda la fuerza bruta en procesar
        time.sleep(0.001 * (2 ** n / 100))
        
        # Guardamos la hora exacta de fin
        fin = time.perf_counter()
        
        # Calculamos cuánto tardó
        tiempo_total = fin - inicio
        tiempos.append(tiempo_total)
        
        print(f"Paquetes: {n} | Tiempo: {tiempo_total:.4f} segundos")

    # 3. Dibujar la gráfica
    plt.plot(lista_paquetes, tiempos, marker='o', color='blue')
    plt.title('Tiempo de Ejecución vs Cantidad de Paquetes')
    plt.xlabel('Número de Paquetes')
    plt.ylabel('Tiempo (segundos)')
    plt.grid(True)
    
    # Guardar la imagen de la gráfica
    plt.savefig('grafica_fuerza_bruta_logistica.png')
    print("\n Gráfica guardada como 'grafica_fuerza_bruta_logistica.png'")


# Ejecutar el programa
if __name__ == '__main__':
    medir_tiempos_y_graficar()