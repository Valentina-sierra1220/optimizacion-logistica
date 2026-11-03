# Optimización Logística: Asignación y Ruteo de Paquetes

**Asignatura:** Análisis y Diseño de Algoritmos  
**Proyecto:** Sistema de Logística y Distribución de Paquetes  
**Integrantes:** Valentina Sierra, María Jose Hincapie  
**Fecha:** Octubre 2026  

---

## 📌 Descripción del Proyecto

Este proyecto aborda la optimización integral del proceso de distribución de paquetes para un servicio de paquetería urbana. El objetivo principal es resolver simultáneamente:

1. **Asignación de Carga:** Asignar $n$ paquetes a una flota de $m$ camiones asegurando no exceder la capacidad de carga útil de cada vehículo ($\sum \text{peso} \le \text{capacidad}$).
2. **Ruteo de Entregas (TSP):** Encontrar el orden óptimo de entrega por camión ($k!$ permutaciones) para garantizar que el tiempo de llegada respete las ventanas de atención exigidas por cada cliente (`ventana_inicio` a `ventana_fin`).

---

## 🚀 Estrategias de Solución Implementadas

### 1. Fuerza Bruta (Entrega 1)
* **Objetivo:** Generar exhaustivamente todas las posibles asignaciones de paquetes a camiones ($m^n$), evaluar las secuencias de entrega y verificar qué combinaciones respetan las capacidades máximas de carga y las ventanas de horario permitidas.
* **Garantía:** Asegura el óptimo global y sirve como línea base (*baseline*) del proyecto.

### 2. Solución Heurística Greedy / Voraz (Entrega 2)
* **Objetivo:** Resolver la asignación y ruteo mediante decisiones locales e irreversibles en dos etapas:
  1. **Organización:** Ordenar los paquetes según la ventana de tiempo más próxima (`ventana_inicio`).
  2. **Selección:** Asignar de inmediato cada paquete al primer camión disponible que cumpla con la capacidad de carga y permita un ruteo en horario.
* **Garantía:** Proporciona tiempos de ejecución casi instantáneos ($\mathcal{O}(n \log n)$), aunque no garantiza el óptimo global en todos los escenarios debido a su naturaleza miope.

---

## 📁 Estructura del Repositorio

```text
optimizacion-logistica/
├── datos/                      # Archivos de entrada (.txt) reales en formato JSON
│   ├── caso_pequeno.txt
│   ├── caso_mediano.txt
│   └── caso_grande.txt
├── docs/                       # Informes técnicos y documentación del proyecto
│   ├── entrega1.md
│   └── entrega2.md
├── src/                        # Código fuente del proyecto
│   ├── fuerza_bruta.py         # Algoritmo de Fuerza Bruta (Asignación + Ruteo)
│   ├── greedy.py               # Algoritmo Voraz / Greedy
│   ├── comparativa.py          # Script de benchmarking y generación de métricas
│   └── grafica_comparativa.png # Gráfica de rendimiento generada
└── README.md                   # Documentación principal




1. Descripción del Conjunto de Datos y Casos de PruebaPara la validación y evaluación experimental de los algoritmos, se estructuraron tres casos de prueba en formato JSON/TXT ubicados en el directorio datos/:datos/caso_pequeno.txtdatos/caso_mediano.txtdatos/caso_grande.txtCada caso de prueba parametriza completamente las restricciones del problema de logística:Flota de Camiones: Capacidad máxima de carga útil ($\text{peso}$) y hora de salida desde el depósito.Paquetes: Peso individual, nodo de destino, tiempo de viaje desde el depósito, tiempo de atención/descarga y ventanas de tiempo requeridas ($\text{ventana\_inicio}$ a $\text{ventana\_fin}$).

📄 Ejemplo de Estructura de Datos (datos/caso_grande.txt)


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



