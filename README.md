# Optimización Logística: Asignación y Ruteo de Paquetes

**Asignatura:** Análisis y Diseño de Algoritmos  
**Proyecto:** Sistema de Logística y Distribución de Paquetes  
**Integrantes:** Valentina Sierra, María Jose Hincapie  
**Fecha:** Octubre 2026  

---

## 📌 Descripción del Proyecto

Este proyecto aborda la optimización integral del proceso de distribución de paquetes para un servicio de paquetería urbana. El objetivo principal es resolver simultáneamente:

1. **Asignación de Carga (Bin Packing):** Asignar $n$ paquetes a una flota de $m$ camiones asegurando no exceder la capacidad de carga útil de cada vehículo ($\sum \text{peso} \le \text{capacidad}$).
2. **Ruteo de Entregas (TSP con Ventanas de Tiempo):** Encontrar el orden óptimo de entrega por camión ($k!$ permutaciones) para garantizar que el tiempo de llegada respete las ventanas de atención exigidas por cada cliente (`ventana_inicio` a `ventana_fin`).

---

## 🚀 Estrategias de Solución Implementadas

### 1. Fuerza Bruta (Entrega 1)
- **Objetivo:** Generar exhaustivamente todas las posibles asignaciones de paquetes a camiones ($m^n$), evaluar las secuencias de entrega y verificar qué combinaciones respetan las capacidades máximas de carga y las ventanas de horario permitidas.
- **Complejidad:** $\mathcal{O}(m^n \cdot m \cdot k! \cdot k)$
- **Garantía:** Asegura el óptimo global y sirve como línea base (*baseline*) del proyecto, aunque se vuelve inviable para instancias con $n \ge 18$.

### 2. Solución Heurística Greedy / Voraz (Entrega 2)
- **Objetivo:** Resolver la asignación y ruteo mediante decisiones locales e irreversibles en dos etapas:
  1. **Organización:** Ordenar los paquetes según la ventana de tiempo más próxima (`ventana_inicio`).
  2. **Selección:** Asignar de inmediato cada paquete al primer camión disponible que cumpla con la capacidad de carga y permita un ruteo en horario.
- **Complejidad:** $\mathcal{O}(n \log n)$
- **Garantía:** Proporciona tiempos de ejecución casi instantáneos en el orden de milisegundos, ideal para alta escalabilidad.

### 3. Solución Divide y Vencerás (Entrega 3)
- **Objetivo:** Descomponer la validación de pesos y capacidades en subproblemas recursivos independientes por mitades (fases: dividir, vencer y combinar).
- **Complejidad:** $\mathcal{O}(n)$
- **Garantía:** Demuestra una estabilidad superior y un rendimiento sumamente eficiente frente al crecimiento del volumen de datos.

---

## 📁 Estructura del Repositorio

```text
optimizacion-logistica/
├── datos/                                  # Casos de prueba reales (.txt / .json)
│   ├── caso_pequeno.txt                    # n = 6 paquetes, m = 2 camiones
│   ├── caso_mediano.txt                    # n = 12 paquetes, m = 3 camiones
│   ├── caso_grande.txt                     # n = 18 paquetes, m = 4 camiones
│   └── caso_estres.txt                     # n = 24 paquetes, m = 5 camiones
├── docs/                                   # Informes técnicos y documentación oficial
│   ├── entrega1.pdf
│   ├── entrega2.pdf
│   └── entrega3_final.pdf
├── src/                                    # Código fuente del proyecto
│   ├── fuerza_bruta.py                     # Algoritmo de Fuerza Bruta
│   ├── greedy.py                           # Algoritmo Voraz / Greedy
│   ├── backtracking.py                     # Algoritmo con Poda (Backtracking)
│   ├── divide_y_venceras.py                # Algoritmo Divide y Vencerás
│   ├── comparativa.py                      # Script de benchmarking y métricas
│   ├── grafica_fuerza_bruta_logistica.png  # Gráfica de rendimiento (Fuerza Bruta)
│   ├── grafica_greedy_logistica.png        # Gráfica de rendimiento (Greedy)
│   └── grafica_divide_y_venceras_logistica.png # Gráfica de rendimiento (D&V)
└── README.md                               # Documentación principal




## 📊 Descripción del Conjunto de Datos y Casos de Prueba

Para la validación y evaluación experimental de los algoritmos, se estructuraron cuatro casos de prueba ubicados en el directorio `datos/`:

* `caso_pequeno.txt` (`n = 6`)
* `caso_mediano.txt` (`n = 12`)
* `caso_grande.txt` (`n = 18`)
* `caso_estres.txt` (`n = 24`)

Cada caso de prueba parametriza completamente las restricciones del problema logístico:

* **Flota de Camiones:** Capacidad máxima de carga útil y hora operativa de inicio/fin.
* **Paquetes:** Peso individual, nodo de destino, tiempo de viaje desde el depósito, tiempo de entrega y ventanas de tiempo requeridas (`ventana_inicio` a `ventana_fin`).


### 📄 Ejemplo de Estructura de Datos (`datos/caso_grande.txt`)[cite: 1]

```json
{
  "camiones": [
    { "id": "C1", "capacidad": 45, "hora_inicio": 6, "hora_fin": 22 },
    { "id": "C2", "capacidad": 45, "hora_inicio": 7, "hora_fin": 23 },
    { "id": "C3", "capacidad": 45, "hora_inicio": 8, "hora_fin": 23 },
    { "id": "C4", "capacidad": 45, "hora_inicio": 9, "hora_fin": 23 }
  ],
  "paquetes": [
    {
      "id": "P1",
      "peso": 8,
      "destino": "D1",
      "ventana_inicio": 8,
      "ventana_fin": 14,
      "tiempo_viaje": 1,
      "tiempo_entrega": 1
    },
    {
      "id": "P2",
      "peso": 7,
      "destino": "D2",
      "ventana_inicio": 9,
      "ventana_fin": 16,
      "tiempo_viaje": 1,
      "tiempo_entrega": 1
    }
  ]
}



## ⚙️ Instrucciones de Ejecución

Para ejecutar las mediciones empíricas de tiempos y actualizar de forma automática las gráficas de rendimiento de los algoritmos implementados, ejecuta el siguiente comando desde la raíz del proyecto:

```bash
python3 src/comparativa.py