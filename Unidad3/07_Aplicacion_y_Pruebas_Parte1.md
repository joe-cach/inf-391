# Unidad 3: Aplicación Práctica y Pruebas de Escritorio (Parte 1)

**Enfoque:** Integración de la teoría matemática pura a la arquitectura del diagrama de flujo mediante la ejecución algorítmica manual (*Desk Checking*).

> **Cita Académica Clave:** > Pegden, C. D., Shannon, R. E., & Sadowski, R. P. (1995). *Introduction to Simulation Using SIMAN* (2da ed.). McGraw-Hill. 
> *(El Capítulo 3 establece la obligatoriedad de la traza manual de eventos antes de escribir la primera línea de código en un simulador).*

---

## 3.6.1. Mapeo Arquitectónico: Inyectando Variables

Hasta ahora, poseemos un diagrama de flujo estático (Unidad 2) y un catálogo de fórmulas estadísticas (Unidad 3). El primer paso en la aplicación práctica es el **Mapeo Arquitectónico**: determinar exactamente en qué nodo del sistema se inyectará cada fórmula. 

Aplicamos la siguiente "Regla de Oro" sobre nuestro diagrama:

1. **El Evento de Llegada (La Flecha Inicial):** ¿Cada cuánto tiempo entra una entidad al sistema?
   * *Inyección:* Variable **Continua** (Casi siempre *Exponencial*).
2. **Los Rombos de Decisión (Bifurcaciones):** ¿Qué camino toma la entidad o qué tipo de error tiene?
   * *Inyección:* Variable **Discreta** (*Bernoulli* para 2 caminos, *Empírica* para múltiples).
3. **Los Rectángulos de Proceso (El *Delay*):** ¿Cuántos milisegundos retendrá el servidor a esta entidad antes de liberarla?
   * *Inyección:* Variable **Continua** (*Uniforme, Normal o Triangular*).

---

## 3.6.2. La Prueba de Escritorio (*Desk Check*)

Antes de abrir el IDE de Python o una hoja de Excel, la arquitectura del simulador debe validarse en papel. A esto se le llama **Prueba de Escritorio**. 

¿Por qué se exige este paso en simulación?
* **Destruye la "Magia" del Código:** Si un programador usa la librería `random.choices()` en Python, asume que la computadora es inteligente. Al hacerlo a mano, el programador comprende que el azar es solo una estricta evaluación de inecuaciones matemáticas.
* **Valida el Algoritmo:** Permite auditar si los parámetros $\beta$ (promedios) y $p$ (probabilidades) están generando comportamientos físicos coherentes antes de iterarlos un millón de veces en la memoria RAM.

Para realizar la prueba, se debe actuar como la CPU: asume una lista de números crudos $U(0,1)$ pre-generados y procesa matemáticamente el viaje de las entidades paso a paso.

---

## 3.6.3. Caso de Estudio 1: Ruteo Lógico (El API Gateway)

**El Escenario:**
Estamos modelando el enrutador de entrada de nuestra arquitectura de microservicios. Cuando un paquete HTTP llega al rombo de decisión, el balanceador debe derivarlo a uno de tres servicios basándose en el tráfico histórico:
* **Autenticación (Auth):** Recibe el 20% del tráfico.
* **Consultas (Query):** Recibe el 50% del tráfico.
* **Mutaciones (Write):** Recibe el 30% del tráfico.

**Paso 1: Construcción del Modelo Matemático (Empírica Discreta)**
Apilamos las probabilidades para crear la métrica de decisión $F(x)$:
* Rango Auth: $0.00$ a $0.20$
* Rango Query: $0.21$ a $0.70$
* Rango Write: $0.71$ a $1.00$

**Paso 2: Ejecución Manual**
Nuestra "CPU mental" genera tres números pseudoaleatorios para los primeros tres paquetes de red que llegan al Gateway.

* **Paquete 1 (El motor genera $U_1 = 0.65$):**
  * *Evaluación Lógica:* $0.65$ es mayor a $0.20$ pero menor a $0.70$.
  * *Resolución Física:* El Paquete 1 es enrutado al microservicio **Query**.
* **Paquete 2 (El motor genera $U_2 = 0.15$):**
  * *Evaluación Lógica:* $0.15$ es menor o igual a $0.20$.
  * *Resolución Física:* El Paquete 2 es enrutado al microservicio **Auth**.
* **Paquete 3 (El motor genera $U_3 = 0.88$):**
  * *Evaluación Lógica:* $0.88$ cae en el último tercio de la tabla (mayor a $0.70$).
  * *Resolución Física:* El Paquete 3 es enrutado al microservicio **Write**.

*Conclusión del Caso 1: Hemos comprobado que el algoritmo de ruteo funciona perfectamente y está listo para ser programado en código duro.*

---

## 3.6.4. Caso de Estudio 2: Cronometría (El Servidor / Autolavado)

**El Escenario:**
Evaluamos el rectángulo de proceso y las llegadas de un nodo físico (aplicable a una bahía de lavado o al procesador de un servidor).
* **Llegadas:** Los clientes (o peticiones) llegan siguiendo un comportamiento *Exponencial*, con un promedio de $\beta = 10$ minutos. Su fórmula generadora despejada es $X = -10 \ln(1 - U)$.
* **Procesamiento:** El tiempo de servicio es exacto y mecánico. Sigue una distribución *Uniforme Continua* entre $a = 4$ y $b = 6$ minutos. Su fórmula generadora despejada es $X = 4 + U \cdot (6 - 4) = 4 + 2U$.

**Paso 1: Dinámica de la Entidad 1**
Llega el primer cliente. ¿Cuánto tiempo se demoró en llegar respecto al inicio de la simulación?
* El motor genera $U_1 = 0.35$.
* *Cálculo de Llegada:* $X_{\text{llegada}} = -10 \cdot \ln(1 - 0.35) \implies X = -10 \cdot \ln(0.65) \implies \mathbf{4.30 \text{ minutos}}$.
* El cliente entra inmediatamente a la máquina. ¿Cuánto tiempo exacto de CPU / Bahía consumirá?
* El motor necesita un número nuevo e independiente para el proceso, genera $U_2 = 0.80$.
* *Cálculo de Proceso:* $X_{\text{proceso}} = 4 + 2(0.80) \implies 4 + 1.6 \implies \mathbf{5.60 \text{ minutos}}$.

**Paso 2: Dinámica de la Entidad 2**
Llega el segundo cliente. ¿Cuánto tiempo transcurrió *desde* que llegó el primer cliente?
* El motor genera $U_3 = 0.90$.
* *Cálculo de Llegada:* $X_{\text{llegada}} = -10 \cdot \ln(1 - 0.90) \implies -10 \cdot \ln(0.10) \implies \mathbf{23.02 \text{ minutos}}$.
* Al entrar al servicio, ¿cuánto tiempo tomará?
* El motor genera $U_4 = 0.10$.
* *Cálculo de Proceso:* $X_{\text{proceso}} = 4 + 2(0.10) \implies 4 + 0.2 \implies \mathbf{4.20 \text{ minutos}}$.

*Conclusión del Caso 2: Hemos demostrado cómo las ecuaciones transforman un decimal estéril en un cronómetro físico real, probando que el sistema puede generar desde procesos muy rápidos (4.20 mins) hasta sequías donde no llega nadie por mucho tiempo (23 mins), replicando el caos estructurado del mundo real.*