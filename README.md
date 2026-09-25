# Optimización Logística: Asignación y Ruteo de Paquetes

**Asignatura:** Análisis y Diseño de Algoritmos  
**Proyecto:** Sistema de Logística y Distribución de Paquetes  
**Integrantes:** Valentina Sierra, María Jose Hincapie  
**Fecha:** Septiembre 2026  

---

## 📌 Descripción del Proyecto

Este proyecto aborda la optimización integral del proceso de distribución de paquetes para un servicio de paquetería urbana. El objetivo principal es resolver simultáneamente:

1. **Asignación de Carga:** Asignar $n$ paquetes a una flota de $m$ camiones asegurando no exceder la capacidad de carga útil de cada vehículo ($\sum \text{peso} \le \text{capacidad}$).
2. **Ruteo de Entregas (TSP):** Encontrar el orden óptimo de entrega por camión ($k!$ permutaciones) para garantizar que el tiempo de llegada respete las ventanas de atención exigidas por cada cliente (`ventana_inicio` a `ventana_fin`).

> **Objetivo de la Solución de Fuerza Bruta:**  
> Generar exhaustivamente todas las posibles asignaciones de paquetes a camiones, evaluar las secuencias de entrega y verificar qué combinaciones respetan las capacidades máximas de carga y las ventanas de horario permitidas de cada cliente.

## 📁 Estructura del Repositorio

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





## 1. Descripción del Conjunto de Datos y Casos de Prueba

Para la validación y evaluación experimental del algoritmo, se estructuraron tres casos de prueba en formato JSON/TXT ubicados en el directorio `datos/`:

* `datos/caso_pequeno.txt`
* `datos/caso_mediano.txt`
* `datos/caso_grande.txt`

Cada caso de prueba parametriza completamente las restricciones del problema de logística:
* **Flota de Camiones:** Capacidad máxima de carga útil ($\text{peso}$) y hora de salida desde el depósito.
* **Paquetes:** Peso individual, nodo de destino, tiempo de viaje desde el depósito, tiempo de atención/descarga y **ventanas de tiempo** requeridas ($\text{ventana\_inicio}$ a $\text{ventana\_fin}$).

---

### 📄 Ejemplo de Estructura de Datos (`datos/caso_grande.txt`)

```json
{
  "camiones": [
    { "id": "C1", "capacidad": 30, "hora_inicio": 8 },
    { "id": "C2", "capacidad": 25, "hora_inicio": 8 },
    { "id": "C3", "capacidad": 20, "hora_inicio": 8 },
    { "id": "C4", "capacidad": 30, "hora_inicio": 8 }
  ],
  "paquetes": [
    {
      "id": "P1",
      "peso": 7,
      "destino": "D1",
      "ventana_inicio": 9,
      "ventana_fin": 11,
      "tiempo_viaje": 1,
      "tiempo_entrega": 1
    },
    {
      "id": "P2",
      "peso": 12,
      "destino": "D2",
      "ventana_inicio": 10,
      "ventana_fin": 12,
      "tiempo_viaje": 1,
      "tiempo_entrega": 1
    },
    {
      "id": "P3",
      "peso": 5,
      "destino": "D3",
      "ventana_inicio": 11,
      "ventana_fin": 13,
      "tiempo_viaje": 2,
      "tiempo_entrega": 1
    },
    {
      "id": "P4",
      "peso": 9,
      "destino": "D4",
      "ventana_inicio": 12,
      "ventana_fin": 14,
      "tiempo_viaje": 2,
      "tiempo_entrega": 1
    }
  ]
}


## 2. 🚀 Instrucciones de Ejecución

Para reproducir las pruebas de rendimiento, ejecutar la medición empírica de tiempos sobre los archivos de prueba reales (`caso_pequeno.txt`, `caso_mediano.txt` y `caso_grande.txt`) y regenerar automáticamente la gráfica de resultados, ejecuta el siguiente comando desde la raíz del proyecto:

```bash
python3 src/comparativa.py


## 3. 🧮 Análisis de Complejidad Teórica

### ⏱️ Complejidad Temporal: $\mathcal{O}(m^n \cdot m \cdot k! \cdot k \cdot n)$
Para un total de $n$ paquetes y $m$ camiones, el algoritmo explora exhaustivamente $m^n$ combinaciones de asignación. Para cada camión que recibe $k$ paquetes ($\sum k = n$), el sistema evalúa hasta $k!$ permutaciones de ruteo para verificar el cumplimiento estricto de las ventanas de tiempo ($\text{ventana\_inicio}$ a $\text{ventana\_fin}$). Esto produce una explosión combinatoria que vuelve inviable el algoritmo para instancias grandes.

### 💾 Complejidad Espacial: $\mathcal{O}(m^n \cdot n + n!)$
El consumo de memoria es directamente proporcional a la profundidad de la pila de llamadas recursivas ($\mathcal{O}(n)$) sumado al espacio requerido para almacenar el conjunto global de soluciones válidas en el peor escenario, donde cada solución retiene las asignaciones correspondientes.


## 4. 📊 Análisis Empírico de Tiempos de Ejecución

Se realizó una medición experimental de los tiempos de ejecución evaluando el desempeño del algoritmo sobre las tres instancias de prueba del proyecto:

| Caso de Prueba | Archivo Evaluado | Asignaciones Evaluadas | Soluciones Válidas Encontradas | Tiempo de Ejecución (s) |
| :--- | :--- | :---: | :---: | :---: |
| **Pequeño** | `caso_pequeno.txt` | $16$ | $1$ | $\approx 0.0000$ |
| **Mediano** | `caso_mediano.txt` | $6,561$ | $6$ | $\approx 0.0243$ |
| **Grande** | `caso_grande.txt` | $16,777,216$ | $382,032$ | $\approx 148.8030$ |

---

### 📈 Gráfica de Rendimiento

![Gráfica de Tiempos de Ejecución](src/grafica_fuerza_bruta_logistica.png)

---

### 📝 Interpretación de Resultados

1. **Casos Pequeño y Mediano:** La ejecución se completa en fracciones de segundo ($\approx 0.0000\text{ s}$ y $\approx 0.0243\text{ s}$) debido al bajo número de permutaciones y asignaciones a evaluar ($16$ y $6,561$).
2. **Caso Grande:** Al incrementar el espacio de búsqueda a $16,777,216$ asignaciones, el tiempo de procesamiento se dispara hasta los **$148.8030\text{ segundos}$ ($\approx 2.5\text{ minutos}$)**.
3. **Conclusión:** El experimento evidencia la explosión combinatoria propia de la Fuerza Bruta, demostrando la necesidad imperativa de implementar estrategias de optimización como poda por *Backtracking*, algoritmos voraces (*Greedy*) o metaheurísticas para las próximas entregas.



1. 📄 Descripción del Conjunto de Datos y Casos de Prueba
Para la validación y evaluación experimental del algoritmo, se estructuraron tres casos de prueba en formato JSON/TXT ubicados en el directorio datos/:

datos/caso_pequeno.txt

datos/caso_mediano.txt

datos/caso_grande.txt

Cada caso de prueba parametriza completamente las restricciones del problema de logística:

Flota de Camiones: Capacidad máxima de carga útil (peso) y hora de salida desde el depósito.

Paquetes: Peso individual, nodo de destino, tiempo de viaje desde el depósito, tiempo de atención/descarga y ventanas de tiempo requeridas (ventana_inicio a ventana_fin).