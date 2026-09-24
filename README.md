# Caso de Estudio: Optimización Logística (Sistema de Logística y Entregas)

> ## Objetivo de la Solución de Fuerza Bruta
> 
> Generar exhaustivamente todas las posibles asignaciones de paquetes a camiones, evaluar las secuencias de entrega y verificar qué combinaciones respetan las capacidades máximas de carga de los camiones, así como las ventanas de horario permitidas de cada cliente, devolviendo las soluciones válidas.

---

> ## 1. Descripción del Conjunto de Datos y Casos de Prueba
> 
> Para la validación y pruebas del algoritmo de asignación y ruteo logístico de paquetes a camiones, se estructuraron tres casos de prueba en formato JSON/TXT ubicados en la carpeta `datos/`: `caso_pequeno.json`, `caso_mediano.json` y `caso_grande.json`.
> 
> Cada archivo contempla la capacidad física y hora de salida de la flota de camiones, así como los pesos, destinos, tiempos de traslado y ventanas de horario para la entrega de cada paquete (cubriendo la asignación, ruteo y restricciones de tiempo).
> 
> Ejemplo de la estructura de datos utilizada (`datos/caso_grande.json`):
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
> * **Complejidad Temporal: $\mathcal{O}(m^n \cdot n)$**  
>   Para $n$ paquetes y $m$ camiones, existen $m^n$ combinaciones de asignación posibles. En cada paso recursivo se realiza una copia del estado actual del diccionario de tamaño $n$, añadiendo un costo lineal $\mathcal{O}(n)$, resultando en un tiempo de ejecución puramente exponencial.
> 
> * **Complejidad Espacial: $\mathcal{O}(n^2)$**  
>   La pila de llamadas recursivas alcanza una profundidad máxima de $n$ niveles. Como en cada marco de ejecución se almacena una copia local del diccionario de asignaciones con tamaño proporcional al nivel actual, la memoria auxiliar ocupada suma $\sum_{i=1}^{n} i = \mathcal{O}(n^2)$.

---

> ## 4. Análisis Empírico de Tiempos de Ejecución
> 
> Se realizó una medición experimental de tiempos de ejecución variando la cantidad de paquetes ($n$) desde $n = 2$ hasta $n = 12$.
> 
> ![Gráfica de Tiempos de Ejecución](src/grafica_fuerza_bruta_logistica.png)
> 
> Como se observa en la gráfica, el tiempo transcurrido aumenta de forma vertiginosa a medida que crece $n$. Esto confirma empíricamente la complejidad teórica del algoritmo de Fuerza Bruta ($\mathcal{O}(m^n \cdot n)$), demostrando que el tiempo de procesamiento se vuelve inviable para instancias grandes de paquetes.