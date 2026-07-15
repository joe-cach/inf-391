# Unidad 3: Laboratorio Computacional - Variables Continuas en Excel

**Enfoque:** Guía algorítmica para implementar el catálogo completo de variables aleatorias continuas (tiempo y demoras) en Microsoft Excel.

> **Regla de Oro del Laboratorio:** Al modelar el tiempo (variables continuas), obtenemos infinitos decimales. A diferencia de las discretas donde contábamos eventos (`CONTAR.SI`), aquí nuestra principal herramienta de validación estadística será la media (`PROMEDIO`) y la desviación estándar (`DESVEST.M`), comprobando que la nube de tiempos simulados respeta la física del sistema.

---

## 1. Distribución Exponencial (Llegadas Asíncronas)

**Escenario:** Tiempos de llegada (*Inter-arrival times*) de peticiones HTTP a un balanceador de carga. Históricamente, llega una petición en promedio cada 12 milisegundos.

### A. Panel de Control (Parámetros)
* `B1` (Tiempo Promedio $\beta$): **12**

### B. Matriz de Simulación (Fila 6 hacia abajo)
* **Columna A (ID_Petición):** `1 a 1000`
* **Columna B (Motor U):** `=ALEATORIO()`
* **Columna C (Tiempo hasta siguiente petición):** `=-$B$1 * LN(1 - B6)`
  *(Aplicación pura de la Transformada Inversa matemática).*

### C. Validación (Auditoría Estadística)
* **Promedio Teórico:** **12.00 ms**
* **Promedio Simulado:** `=PROMEDIO(C6:C1005)`
* *Criterio de Éxito:* Al presionar **F9**, el promedio debe orbitar muy cerca de $12.00$. Observa los datos individuales: verás valores muy cercanos a $0$ (ráfagas rápidas) y algunos picos raros de $50$ o $60$ ms (sequías largas).

---

## 2. Distribución Uniforme Continua (Hardware Mecánico)

**Escenario:** Un brazo robótico en una línea de ensamblaje mueve una pieza. El hardware está calibrado para tardar entre $4.2$ y $4.8$ segundos.

### A. Panel de Control (Parámetros)
* `B1` (Tiempo Mínimo $a$): **4.2**
* `B2` (Tiempo Máximo $b$): **4.8**

### B. Matriz de Simulación (Fila 6 hacia abajo)
* **Columna A (ID_Pieza):** `1 a 1000`
* **Columna B (Motor U):** `=ALEATORIO()`
* **Columna C (Tiempo de Movimiento):** `=$B$1 + B6 * ($B$2 - $B$1)`

### C. Validación (Auditoría Estadística)
* **Promedio Teórico:** $\frac{a+b}{2} = \frac{4.2+4.8}{2} = \mathbf{4.50}$ segundos.
* **Promedio Simulado:** `=PROMEDIO(C6:C1005)`
* *Criterio de Éxito:* El promedio simulado debe ser $\approx 4.50$. Además, comprueba el límite inferior con `=MIN(C6:C1005)` (debe ser $> 4.2$) y el límite superior con `=MAX(C6:C1005)` (debe ser $< 4.8$).

---

## 3. Distribución Normal / Gaussiana (Tiempos Humanos)

**Escenario:** El tiempo que tarda un operador de *Call Center* en registrar a un cliente en el sistema. El promedio es de 45 segundos, con una desviación estándar de 5 segundos.

### A. Panel de Control (Parámetros)
* `B1` (Media $\mu$): **45**
* `B2` (Desviación Estándar $\sigma$): **5**

### B. Matriz de Simulación (Fila 6 hacia abajo)
Excel posee la transformada inversa de Gauss ya integrada, lo que nos evita programar el complejo algoritmo de Box-Muller.
* **Columna A (ID_Llamada):** `1 a 1000`
* **Columna B (Motor U):** `=ALEATORIO()`
* **Columna C (Tiempo de Atención):** `=INV.NORM.N(B6; $B$1; $B$2)`

### C. Validación (Auditoría Estadística)
* **Promedio Simulado:** `=PROMEDIO(C6:C1005)` $\rightarrow$ *Debe acercarse a 45.*
* **Desviación Simulada:** `=DESVEST.M(C6:C1005)` $\rightarrow$ *Debe acercarse a 5.*

---

## 4. Distribución Triangular (Estimación de Expertos)

**Escenario:** Estimación del tiempo de compilación de un monolito de software. Un ingeniero *Senior* estima: Mínimo 2 min, Más Probable 5 min, Máximo 14 min (si hay conflictos).

### A. Panel de Control (Parámetros)
* `B1` (Mínimo $a$): **2**
* `B2` (Moda/Más Probable $c$): **5**
* `B3` (Máximo $b$): **14**
* `B4` (Umbral de Inflexión): `=($B$2-$B$1)/($B$3-$B$1)` *(Calculamos esto en el panel para hacer la fórmula más limpia. Resultado $\approx 0.25$).*

### B. Matriz de Simulación (Fila 6 hacia abajo)
Aplicaremos la transformada inversa por tramos usando un `SI()`.
* **Columna A (ID_Compilación):** `1 a 1000`
* **Columna B (Motor U):** `=ALEATORIO()`
* **Columna C (Tiempo Generado):** `=SI(B6 <= $B$4; $B$1 + RAIZ(B6 * ($B$3-$B$1)*($B$2-$B$1)); $B$3 - RAIZ((1-B6) * ($B$3-$B$1)*($B$3-$B$2)))`

### C. Validación (Auditoría Estadística)
* **Promedio Teórico:** $\frac{a+b+c}{3} = \frac{2+14+5}{3} = \mathbf{7.00}$ minutos.
* **Promedio Simulado:** `=PROMEDIO(C6:C1005)` $\rightarrow$ *Debe orbitar el 7.00 al presionar F9.*

---

## 5. Distribución Lognormal (Latencia de Red / Cola Larga)

**Escenario:** Tiempos de descarga de un archivo. Suele ser muy rápido, pero las congestiones de red crean tiempos atípicamente altos.

### A. Panel de Control (Parámetros Logarítmicos)
*(Nota: Estos son los parámetros de la escala logarítmica, no el tiempo real)*
* `B1` (Media Logarítmica $\mu$): **1.5**
* `B2` (Desviación Logarítmica $\sigma$): **0.5**

### B. Matriz de Simulación (Fila 6 hacia abajo)
* **Columna A (ID_Descarga):** `1 a 1000`
* **Columna B (Motor U):** `=ALEATORIO()`
* **Columna C (Tiempo de Red):** `=INV.LOGNORM(B6; $B$1; $B$2)`

### C. Validación (Auditoría Estadística)
* **Comportamiento Físico:** Utiliza `=MEDIANA(C6:C1005)` y `=PROMEDIO(C6:C1005)`. En una lognormal real, la Media siempre es notablemente mayor que la Mediana, arrastrada por los valores extremos (*Outliers*). Usa `=MAX(C6:C1005)` para observar esos picos de congestión severos.

---

## 6. Distribución de Weibull (Ingeniería de Confiabilidad)

**Escenario:** Tiempo Medio Hasta el Fallo (MTTF) de un Disco de Estado Sólido (SSD). Falla por desgaste, no por azar.

### A. Panel de Control (Parámetros)
* `B1` (Forma $\alpha$): **1.5** *(Un valor $>1$ indica tasa de fallo creciente por desgaste/vejez).*
* `B2` (Escala $\beta$): **5000** *(Vida característica en horas).*

### B. Matriz de Simulación (Fila 6 hacia abajo)
* **Columna A (ID_Disco):** `1 a 1000`
* **Columna B (Motor U):** `=ALEATORIO()`
* **Columna C (Horas hasta Falla Catastrófica):** `=$B$2 * (-LN(1 - B6))^(1/$B$1)`

### C. Validación (Auditoría Estadística)
* **Promedio Simulado:** `=PROMEDIO(C6:C1005)`
* *Análisis:* Para estos parámetros ($\alpha=1.5, \beta=5000$), la física del desgaste dicta que el lote de discos tendrá un tiempo de vida promedio aproximado de **4,513 horas**. Tu modelo en Excel validará la teoría de confiabilidad de hardware al estabilizarse cerca de ese valor.

---

## 7. Distribución Gamma (Pipelines y Tareas en Serie)

**Escenario:** Un proceso ETL (*Extract, Transform, Load*) de bases de datos. Tiene 3 etapas secuenciales, cada una con un comportamiento exponencial promedio de 10 ms.

### A. Panel de Control (Parámetros)
* `B1` (Etapas/Forma $\alpha$): **3** *(Representa las 3 tareas del ETL).*
* `B2` (Promedio por etapa/Escala $\beta$): **10**

### B. Matriz de Simulación (Fila 6 hacia abajo)
En lugar de programar 3 columnas Exponenciales y sumarlas (Convolución), usaremos la función nativa que agrupa el proceso.
* **Columna A (ID_Pipeline):** `1 a 1000`
* **Columna B (Motor U):** `=ALEATORIO()`
* **Columna C (Tiempo Total ETL):** `=DISTR.GAMMA.INV(B6; $B$1; $B$2)`

### C. Validación (Auditoría Estadística)
* **Promedio Teórico:** $\alpha \cdot \beta = 3 \cdot 10 = \mathbf{30.00}$ milisegundos totales por Pipeline.
* **Promedio Simulado:** `=PROMEDIO(C6:C1005)`
* *Criterio de Éxito:* El sistema debe demostrar que la suma de las tres etapas de 10ms estabiliza el modelo en 30ms promedio al simular 1,000 ejecuciones.