### Caso de Estudio: "El colapso de la pasarela de pagos"

Un equipo de ingeniería en software recibió el encargo de simular el rendimiento de una nueva pasarela de pagos para el CyberMonday. Asumieron directamente que las peticiones llegarían siguiendo una distribución Uniforme (una petición cada 10 milisegundos). Programaron el simulador rápidamente en Python, lo corrieron una sola vez durante el equivalente a 24 horas simuladas y el sistema no mostró cuellos de botella. El equipo presentó los resultados al directorio y el software fue desplegado a producción. El día del CyberMonday, la pasarela colapsó en los primeros 10 minutos porque las peticiones llegaron en ráfagas masivas (distribución de Poisson) y los hilos de conexión a la base de datos se agotaron. El código del simulador en sí funcionaba perfecto, pero el resultado fue un desastre financiero.

**Preguntas a responder:**
1. ¿Qué pasos exactos de la metodología clásica de simulación fallaron?
2. ¿Por qué el hecho de correr el modelo "una sola vez por 24 horas" carece de validez estadística?

---

### Respuestas

**Pasos que fallaron:**

* **Paso 4 (Recolección de datos / Análisis de Entrada):** Asumieron erróneamente una distribución Uniforme en lugar de analizar datos empíricos históricos de eventos pasados, los cuales habrían mostrado llegadas estocásticas en ráfagas (ej. Poisson/Exponencial).
* **Paso 7 (Validación):** No contrastaron el modelo computacional contra el comportamiento del sistema real en un entorno controlado (Load testing).
* **Paso 8 y 9 (Diseño de Experimentos y Análisis):** Hicieron una sola corrida.

**Falta de validez estadística:**

* Al ser un sistema estocástico, la salida es una variable aleatoria. Una sola corrida es simplemente un punto en una distribución muestral. No permite calcular la varianza ni los intervalos de confianza necesarios para garantizar estadísticamente que el sistema soporta la carga. Se necesitaban múltiples réplicas (corridas) con diferentes semillas aleatorias.