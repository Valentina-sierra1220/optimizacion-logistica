# Optimización Logística - Asignación y Ruteo de Paquetes a Camiones

**Asignatura:** Análisis y Diseño de Algoritmos  
**Proyecto:** Sistema de Logística y Distribución de Paquetes  
**Integrantes:** Valentina Sierra, María Jose Hincapie  
**Fecha:** Septiembre 2026  

---

##  Descripción del Proyecto

Este proyecto aborda la optimización integral del proceso de distribución de paquetes para un servicio de paquetería urbana. El objetivo principal es resolver simultáneamente:

1. **Asignación de Carga:** Asignar $n$ paquetes a una flota de $m$ camiones asegurando no exceder la capacidad de carga útil de cada vehículo ($\sum \text{peso} \le \text{capacidad}$).
2. **Ruteo de Entregas (TSP):** Encontrar el orden óptimo de entrega por camión ($k!$ permutaciones) para garantizar que el tiempo de llegada respete las ventanas de atención exigidas por cada cliente ($\text{ventana\_inicio}$ a $\text{ventana\_fin}$).

# Caso de Estudio: Optimización Logística (Sistema de Logística y Entregas)

> ## Objetivo de la Solución de Fuerza Bruta
> 
> Generar exhaustivamente todas las posibles asignaciones de paquetes a camiones, evaluar las secuencias de entrega y verificar qué combinaciones respetan las capacidades máximas de carga de los camiones, así como las ventanas de horario permitidas de cada cliente, devolviendo las soluciones válidas.

---

##  Estructura del Repositorio

```text

optimizacion-logistica/
├── datos/                      # Archivos de entrada (.txt) reales
│   ├── caso_pequeno.txt
│   ├── caso_mediano.txt
│   └── caso_grande.txt
├── docs/                       # Informes técnicos y documentación del proyecto
│   └── entrega1.md
├── src/                        # Código fuente del proyecto
│   ├── fuerza_bruta.py         # Algoritmo de Fuerza Bruta (Asignación + Ruteo)
│   ├── comparativa.py          # Script de benchmarking y generación de métricas
│   └── grafica_fuerza_bruta_logistica.png  # Gráfica de rendimiento generada
└── README.md                   # Documentación principal

---

> ## 1. Descripción del Conjunto de Datos y Casos de Prueba
> 
> Para la validación y pruebas del algoritmo de asignación y ruteo logístico de paquetes a camiones, se estructuraron tres casos de prueba en formato TXT ubicados en la carpeta `datos/`: `caso_pequeno.txt`, `caso_mediano.txt` y `caso_grande.txt`.
> 
> Cada archivo contempla la capacidad física y hora de salida de la flota de camiones, así como los pesos, destinos, tiempos de traslado y ventanas de horario para la entrega de cada paquete (cubriendo la asignación, ruteo y restricciones de tiempo).
> 
> Ejemplo de la estructura de datos utilizada (`datos/caso_grande.txt`):
> 
> ```json
> {
>   "camiones": [
>     {
>       "id": "C1",
>       "capacidad": 30,
>       "hora_inicio": 8
>     },
>     {
>       "id": "C2",
>       "capacidad": 25,
>       "hora_inicio": 8
>     },
>     {
>       "id": "C3",
>       "capacidad": 20,
>       "hora_inicio": 8
>     },
>     {
>       "id": "C4",
>       "capacidad": 30,
>       "hora_inicio": 8
>     }
>   ],
>   "paquetes": [
>     {
>       "id": "P1",
>       "peso": 7,
>       "destino": "D1",
>       "ventana_inicio": 9,
>       "ventana_fin": 11,
>       "tiempo_viaje": 1,
>       "tiempo_entrega": 1
>     },
>     {
>       "id": "P2",
>       "peso": 12,
>       "destino": "D2",
>       "ventana_inicio": 10,
>       "ventana_fin": 12,
>       "tiempo_viaje": 1,
>       "tiempo_entrega": 1
>     },
>     {
>       "id": "P3",
>       "peso": 5,
>       "destino": "D3",
>       "ventana_inicio": 11,
>       "ventana_fin": 13,
>       "tiempo_viaje": 2,
>       "tiempo_entrega": 1
>     },
>     {
>       "id": "P4",
>       "peso": 9,
>       "destino": "D4",
>       "ventana_inicio": 12,
>       "ventana_fin": 14,
>       "tiempo_viaje": 2,
>       "tiempo_entrega": 1
>     },
>     {
>       "id": "P5",
>       "peso": 15,
>       "destino": "D1",
>       "ventana_inicio": 9,
>       "ventana_fin": 11,
>       "tiempo_viaje": 1,
>       "tiempo_entrega": 1
>     },
>     {
>       "id": "P6",
>       "peso": 3,
>       "destino": "D2",
>       "ventana_inicio": 10,
>       "ventana_fin": 12,
>       "tiempo_viaje": 1,
>       "tiempo_entrega": 1
>     },
>     {
>       "id": "P7",
>       "peso": 8,
>       "destino": "D3",
>       "ventana_inicio": 11,
>       "ventana_fin": 13,
>       "tiempo_viaje": 2,
>       "tiempo_entrega": 1
>     },
>     {
>       "id": "P8",
>       "peso": 10,
>       "destino": "D4",
>       "ventana_inicio": 12,
>       "ventana_fin": 14,
>       "tiempo_viaje": 2,
>       "tiempo_entrega": 1
>     },
>     {
>       "id": "P9",
>       "peso": 6,
>       "destino": "D1",
>       "ventana_inicio": 9,
>       "ventana_fin": 11,
>       "tiempo_viaje": 1,
>       "tiempo_entrega": 1
>     },
>     {
>       "id": "P10",
>       "peso": 11,
>       "destino": "D2",
>       "ventana_inicio": 10,
>       "ventana_fin": 12,
>       "tiempo_viaje": 1,
>       "tiempo_entrega": 1
>     },
>     {
>       "id": "P11",
>       "peso": 4,
>       "destino": "D3",
>       "ventana_inicio": 11,
>       "ventana_fin": 13,
>       "tiempo_viaje": 2,
>       "tiempo_entrega": 1
>     },
>     {
>       "id": "P12",
>       "peso": 14,
>       "destino": "D4",
>       "ventana_inicio": 12,
>       "ventana_fin": 14,
>       "tiempo_viaje": 2,
>       "tiempo_entrega": 1
>     }
>   ]
> }
> ```

---

> ## 2. Instrucciones de Ejecución
> 
> Para ejecutar la medición empírica de tiempos de ejecución y actualizar la gráfica de Fuerza Bruta, ejecuta el siguiente comando desde la raíz del proyecto:
> 
> ```bash
> python3 src/comparativa.py
> ```

---

> ## 3. Análisis de Complejidad Teórica
> 
> * **Complejidad en Tiempo: Exponencial — O(m^n · m · n)**  
>   Si tenemos **n paquetes** y **m camiones**, el algoritmo explora un total de **m^n** combinaciones posibles. En cada llamado recursivo realiza una copia del estado actual de las asignaciones que toma un costo de **n**, y al llegar a cada combinación final (hoja) valida las capacidades de peso recorriendo los **m** camiones y sus **n** paquetes (costo de **m · n**). Esto da un tiempo total proporcional a **m^n · m · n**, haciendo que el tiempo de ejecución explote y se vuelva extremadamente lento al aumentar los paquetes.
> 
> * **Complejidad en Memoria (Espacio): O(m^n · n)**  
>   Durante la ejecución recursiva, el programa alcanza una profundidad de **n** niveles en la pila con una memoria auxiliar de **n²**. Sin embargo, al considerar la estructura global de almacenamiento de resultados, en el peor escenario se guardan las **m^n** soluciones válidas, donde cada solución guarda un diccionario de **n** asignaciones. Esto hace que el consumo global de memoria crezca de forma proporcional a **m^n · n**.


---

## 4. Análisis Empírico de Tiempos de Ejecución

Se realizó una medición experimental de los tiempos de ejecución evaluando el desempeño del algoritmo sobre las tres instancias de prueba del proyecto (`caso_pequeno.txt`, `caso_mediano.txt` y `caso_grande.txt`).

![Gráfica de Tiempos de Ejecución](src/grafica_fuerza_bruta_logistica.png)

Como se observa en los resultados y en la gráfica, el tiempo transcurrido aumenta a un ritmo exponencial a medida que crece el número de asignaciones evaluadas:
- En los casos **Pequeño** ($16$ asignaciones) y **Mediano** ($6,561$ asignaciones), la ejecución toma fracciones de segundo ($\approx 0.000\text{ s}$ y $\approx 0.0243\text{ s}$).
- En el **Caso Grande** ($16,777,216$ asignaciones), el tiempo se dispara hasta alcanzar $\approx 148.803\text{ s}$ ($\approx 2.5\text{ min}$).

Esto confirma empíricamente la complejidad teórica del algoritmo de Fuerza Bruta ($\mathcal{O}(m^n \cdot m \cdot k! \cdot k)$), demostrando la explosión combinatoria que vuelve inviable esta solución para instancias con un número elevado de paquetes.