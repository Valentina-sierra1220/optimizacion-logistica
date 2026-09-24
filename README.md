# Caso de Estudio: Optimización Logística

# objetivo de la solucion de fuerza bruta
Recibir paquetesy camiones para generar todas las posibles asignaciones
de paquetes a camiones , comprobar cuales respetan las capacidades limites de los camiones y devolver las asignacione validas.


## 1. Descripción del Conjunto de Datos y Casos de Prueba

Para la validación y pruebas del algoritmo de asignación logística de paquetes a camiones, se estructuraron tres casos de prueba en formato JSON ubicados en la carpeta `datos/`: `caso_pequeno.json`, `caso_mediano.json` y `caso_grande.json`. Cada archivo contiene la definición de la flota de camiones con sus respectivas capacidades y la lista de paquetes con sus pesos asociados.

Ejemplo de la estructura de datos utilizada:

```json
{
  "camiones": [
    {"id": "C1", "capacidad": 30},
    {"id": "C2", "capacidad": 30}
  ],
  "paquetes": [
    {"id": "P1", "peso": 5},
    {"id": "P2", "peso": 8},
    {"id": "P3", "peso": 12}
  ]
}
```

---



---

## 3. Análisis Empírico de Tiempos de Ejecución

Se realizó una medición experimental de tiempos de ejecución variando la cantidad de paquetes (n) de 2 a 12.

![Gráfica de Tiempos de Ejecución](src/grafica_fuerza_bruta_logistica.png)

Como se observa en la gráfica, el tiempo transcurrido aumenta de forma exponencial a medida que crece n. Esto confirma empíricamente la complejidad teórica del algoritmo de Fuerza Bruta (O(m^n)), demostrando que el tiempo de procesamiento se vuelve inviable para instancias grandes de paquetes.