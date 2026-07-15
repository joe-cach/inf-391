# Unidad 3: Variables Aleatorias Discretas (Parte 2)

**Enfoque:** Algoritmos matemáticos sin decimales para contabilizar entidades, iteraciones, métricas de agrupamiento o fallos en un sistema informático.

> **Cita Académica Clave:** > Law, A. M. (2015). *Simulation Modeling and Analysis* (5ta ed.). McGraw-Hill Education. 
> *(Capítulo 6: Selección de distribuciones de probabilidad teóricas para la contabilización de lotes y eventos).*

---

## El Rol del Conteo en la Simulación

Mientras que en la Parte 1 utilizamos las variables discretas como un "timón" para el ruteo de decisiones (los rombos del diagrama de flujo), en esta Parte 2 nos enfocaremos en la **contabilización**. 

En la ingeniería de software, no siempre evaluamos las entidades una por una de manera individual. A menudo operamos por **lotes** (ej. un *batch* de 1,000 registros de base de datos) o en **ventanas de tiempo** (ej. cuántos errores ocurrieron en la última hora). Las siguientes distribuciones discretas nos permiten generar matemáticamente estos volúmenes de datos agregados en nuestro simulador sin tener que procesar el micro-nivel de cada evento individual, ahorrando valiosos ciclos de reloj.

---

## 3.4. Catálogo de Variables Discretas (Conteo y Lotes)

### 3.4.4. Distribución Binomial

**Definición:**
Si la distribución de Bernoulli (Parte 1) es lanzar una moneda trucada una sola vez, la distribución Binomial es lanzar esa misma moneda $n$ veces y contar cuántas veces salió la cara ganadora. Matemáticamente, es la suma de $n$ experimentos de Bernoulli independientes.

**Componentes Matemáticos:**
* **$n$ (Número de intentos):** El tamaño del lote o la cantidad de pruebas finitas a realizar.
* **$p$ (Probabilidad de éxito):** La probabilidad histórica de que un solo intento sea exitoso.

**El Algoritmo de Generación (Por Convolución):**
En lugar de despejar una fórmula compleja, la forma más intuitiva de programar esto en un motor de simulación es mediante un bucle de sumatoria:
1. Inicializar un contador de éxitos: $X = 0$.
2. Iniciar un bucle `for` que itere $n$ veces.
3. En cada iteración, generar $U \sim \text{Uniform}(0,1)$.
4. Si $U \le p$, sumar $1$ al contador $X$.
5. Al terminar el bucle, retornar $X$.

**¿Para qué sirve en sistemas informáticos?**
Se utiliza para la evaluación de lotes (*Batch Processing*) o el control de calidad de datos.
* *Ejemplos:* Si un microservicio envía un bloque de 500 consultas a la base de datos y la tasa de error de conexión histórica es del 2% ($p = 0.02$), la Binomial nos dirá exactamente cuántas de esas 500 consultas fallaron en esta ejecución específica, sin tener que simular el viaje de red de cada consulta individual.

---

### 3.4.5. Distribución de Poisson

**Definición:**
Es el estándar de la industria para modelar la ocurrencia de eventos aleatorios dentro de un **intervalo de espacio o tiempo estrictamente definido**. A diferencia de la Binomial (que tiene un número fijo de intentos $n$), en Poisson el número de eventos posibles teóricamente tiende al infinito, pero ocurren a una tasa promedio constante.

**Componentes Matemáticos:**
* **$\lambda$ (Lambda):** La tasa de ocurrencia o el promedio histórico de eventos por ventana de tiempo (ej. "llegan 45 clientes por hora").

**El Algoritmo de Generación:**
El algoritmo clásico (Knuth) multiplica números uniformes hasta superar una cota basada en $\lambda$:
1. Calcular el límite: $L = e^{-\lambda}$.
2. Inicializar $k = 0$ y $P = 1$.
3. Bucle `while`:
   * Generar $U \sim \text{Uniform}(0,1)$.
   * $P = P \cdot U$.
   * Si $P > L$, entonces $k = k + 1$ y repetir el bucle.
   * Si $P \le L$, detener.
4. Retornar $k$ (el número de eventos generados para ese bloque de tiempo).

**¿Para qué sirve en sistemas informáticos?**
Es fundamental para modelar volúmenes de tráfico y evaluar el estrés en la infraestructura.
* *Ejemplos:* Calcular cuántos ataques de Fuerza Bruta (DDoS) recibirá un puerto específico entre las 02:00 AM y las 03:00 AM. Contabilizar cuántos *commits* se hacen en un repositorio de código fuente en un día laboral.

---

### 3.4.6. Distribución Geométrica

**Definición:**
Esta distribución contabiliza el número de **fracasos consecutivos que deben ocurrir antes de obtener el primer éxito**. Se basa en repetir un experimento de Bernoulli indefinidamente hasta que la condición se cumpla.

**Componentes Matemáticos:**
* **$p$ (Probabilidad de éxito):** La probabilidad de que el intento actual logre el objetivo deseado.

**El Algoritmo de Generación (Transformada Inversa Analítica):**
A través del álgebra, la Transformada Inversa nos permite calcular la cantidad de iteraciones necesarias en una sola línea de código, evitando un bucle infinito peligroso:
$$X = \left\lfloor \frac{\ln(U)}{\ln(1 - p)} \right\rfloor$$
*(El resultado $X$ representa el número de fracasos previos al éxito).*

**¿Para qué sirve en sistemas informáticos?**
Se utiliza casi exclusivamente para modelar bucles de reintento (*Retry Loops*) o comportamientos de "Encuesta" (*Polling*) en redes inestables.
* *Ejemplos:* Si un microservicio intenta conectarse a un balanceador de carga que se reinicia intermitentemente, y tiene un 15% de probabilidad de conectar ($p = 0.15$), la Geométrica calculará cuántos *Timeouts* (fracasos) sufrirá el hilo de ejecución antes de lograr establecer finalmente el *Socket* TCP.