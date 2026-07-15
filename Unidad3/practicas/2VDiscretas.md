# Unidad 3: Laboratorio Computacional - Variables Discretas en Excel

**Enfoque:** Guía de ejecución algorítmica para implementar el catálogo completo de variables aleatorias discretas en Microsoft Excel, aplicando aislamiento de parámetros y pruebas de validación estadística.

> **Regla de Oro del Laboratorio:** Nunca "quemar" (escribir directamente) parámetros estáticos dentro de la función de una celda. Todo modelo debe tener un **Panel de Control** visible en la parte superior. Las simulaciones deben ejecutarse con un mínimo de $1,000$ filas (entidades) para que la Ley de los Grandes Números funcione.

---

## 1. Distribución de Bernoulli (Decisión de 2 Caminos)

**Escenario:** El *Firewall* de un servidor. El 85% de los paquetes que llegan son válidos, el 15% restante son descartados.

### A. Panel de Control (Parámetros)
* `B1` (Probabilidad de Éxito $p$): **0.85**
* `B2` (Mensaje Éxito): **Válido**
* `B3` (Mensaje Fracaso): **Descartado**

### B. Matriz de Simulación (Fila 6 hacia abajo)
* **Columna A (ID_Paquete):** `1, 2, 3 ... 1000`
* **Columna B (Motor U):** `=ALEATORIO()`
* **Columna C (Decisión Lógica):** `=SI(B6 <= $B$1; $B$2; $B$3)`
  *(Arrastrar hasta la fila 1005).*

### C. Validación (Auditoría Estadística)
* **Paquetes Válidos Simulados:** `=CONTAR.SI(C6:C1005; $B$2)`
* **Probabilidad Simulada:** `=CONTAR.SI(C6:C1005; $B$2) / 1000`
* *Criterio de Éxito:* Al presionar **F9** (Recalcular), la probabilidad simulada debe orbitar muy cerca del parámetro original de $0.85$ (ej. $0.842$, $0.856$).

---

## 2. Distribución Empírica Discreta (Ruteo Múltiple)

**Escenario:** Un *API Gateway* enruta tráfico a tres microservicios según su demanda histórica: Auth (20%), Query (50%), Write (30%).

### A. Panel de Control (Tabla Acumulada $F(x)$)
Para usar el motor de búsqueda de Excel, debemos crear una tabla sumando los porcentajes para definir el límite inferior de cada rango.
*(Asumamos que esto está en el rango `F2:G4`)*
* `F2`: **0.00** | `G2`: **Auth**
* `F3`: **0.20** | `G3`: **Query**
* `F4`: **0.70** | `G4`: **Write**

### B. Matriz de Simulación (Fila 6 hacia abajo)
* **Columna A (ID_Petición):** `1 a 1000`
* **Columna B (Motor U):** `=ALEATORIO()`
* **Columna C (Microservicio Asignado):** `=BUSCARV(B6; $F$2:$G$4; 2; VERDADERO)`
  *(El parámetro VERDADERO le indica a Excel que haga coincidencia aproximada por rangos).*

### C. Validación (Auditoría Estadística)
* **Porcentaje Query Simulado:** `=CONTAR.SI(C6:C1005; "Query") / 1000`
* *Criterio de Éxito:* El resultado debe mantenerse cerca de $0.50$. Insertar un gráfico de barras contando las apariciones de los 3 microservicios para ver visualmente la escalonada empírica.

---

## 3. Distribución Uniforme Discreta (Aleatoriedad Pura)

**Escenario:** Un balanceador de carga puro tipo *Round-Robin* que reparte peticiones entre 4 servidores backend idénticos (numerados del 1 al 4).

### A. Panel de Control (Parámetros)
* `B1` (Límite Inferior $a$): **1**
* `B2` (Límite Superior $b$): **4**

### B. Matriz de Simulación (Fila 6 hacia abajo)
Existen dos formas de hacerlo. La pedagógica (Transformada Inversa) y la nativa de Excel:
* **Columna A (ID_Petición):** `1 a 1000`
* **Columna B (Motor U):** `=ALEATORIO()`
* **Columna C (Forma Inversa):** `=ENTERO(B6 * ($B$2 - $B$1 + 1)) + $B$1`
* **Columna D (Forma Nativa):** `=ALEATORIO.ENTRE($B$1; $B$2)`

### C. Validación (Auditoría Estadística)
* **Frecuencia Servidor 1:** `=CONTAR.SI(C6:C1005; 1) / 1000`
* *Criterio de Éxito:* Dado que hay 4 servidores equiprobables, la métrica para cada uno debe estabilizarse alrededor de $0.25$ (25%).

---

## 4. Distribución Binomial (Lotes)

**Escenario:** Un sistema de *Marketing Automation* envía correos en lotes de 50. La tasa histórica de rebote (*Bounce Rate*) es del 6%. ¿Cuántos correos rebotan exactamente en cada lote?

### A. Panel de Control (Parámetros)
* `B1` (Intentos $n$ - Tamaño de Lote): **50**
* `B2` (Probabilidad Éxito/Fallo $p$): **0.06**

### B. Matriz de Simulación (Fila 6 hacia abajo)
Aquí usaremos la inversa nativa de Excel para evitar programar 50 columnas de Bernoulli.
* **Columna A (ID_Lote):** `1 a 1000` *(Cada fila ahora es un lote entero, no un correo individual).*
* **Columna B (Motor U):** `=ALEATORIO()`
* **Columna C (Correos Rebotados por Lote):** `=DISTR.BINOM.INV($B$1; $B$2; B6)`

### C. Validación (Auditoría Estadística)
* **Promedio Teórico:** $= n \cdot p = 50 \cdot 0.06 = 3.00$ rebotes por lote.
* **Promedio Simulado:** `=PROMEDIO(C6:C1005)`
* *Criterio de Éxito:* Al promediar los 1,000 lotes, el número debe acercarse fuertemente a $3.00$.

---

## 5. Distribución de Poisson (Eventos por Tiempo)

**Escenario:** Simular la cantidad de ataques de denegación de servicio (DDoS) que recibe una IP específica cada hora, sabiendo que el promedio histórico es de $\lambda = 15$ ataques/hora.

### A. Panel de Control (Construcción de Tabla Acumulada Dinámica)
Excel carece de una función simple `INV.POISSON`. El enfoque experto es utilizar el mismo principio de la "Empírica Discreta", generando una tabla matemática automatizada.
* `H1` (Lambda $\lambda$): **15**
* **Tabla de Conversión (Rango `J2:L52`):**
  * `J2` a `J52` (Eventos Posibles $x$): Escribir números del `0` al `50`.
  * `K2` a `K52` (Acumulada $F(x)$): `=DISTR.POISSON.N(J2; $H$1; VERDADERO)`. *(Excel calculará automáticamente el límite inferior de cada probabilidad).*

### B. Matriz de Simulación (Fila 6 hacia abajo)
* **Columna A (Hora_Simulada):** `1 a 1000`
* **Columna B (Motor U):** `=ALEATORIO()`
* **Columna C (Cantidad de Ataques en esa hora):** `=BUSCARV(B6; $K$2:$J$52; 2; VERDADERO)`
  *(Ojo: Para que el buscar funcione, en la columna K debe estar la Probabilidad y en la J los Eventos, intercambiar el orden en la tabla de ser necesario para el BUSCARV, o usar ÍNDICE/COINCIDIR).*

### C. Validación (Auditoría Estadística)
* **Promedio Simulado:** `=PROMEDIO(C6:C1005)`
* *Criterio de Éxito:* El promedio de los ataques por hora en las 1,000 filas debe ser virtualmente idéntico a la Lambda ($\lambda = 15.00$).

---

## 6. Distribución Geométrica (Bucles de Reintento)

**Escenario:** Un microservicio intenta conectarse a una base de datos inestable. Cada intento tiene un 20% de probabilidad de éxito. ¿Cuántos reintentos (*Timeouts*) fallidos sufre antes de lograr conectarse?

### A. Panel de Control (Parámetros)
* `B1` (Probabilidad de Éxito $p$): **0.20**

### B. Matriz de Simulación (Fila 6 hacia abajo)
Aplicaremos la fórmula matemática de la Transformada Inversa explícita: $X = \lfloor \frac{\ln(U)}{\ln(1-p)} \rfloor$
* **Columna A (Conexión_Exitosa_ID):** `1 a 1000`
* **Columna B (Motor U):** `=ALEATORIO()`
* **Columna C (Cant. de Fallos Previos):** `=ENTERO(LN(B6) / LN(1 - $B$1))`

### C. Validación (Auditoría Estadística)
* **Promedio Teórico:** $= \frac{1 - p}{p} = \frac{1 - 0.20}{0.20} = \mathbf{4.00}$ fallos esperados antes del éxito.
* **Promedio Simulado:** `=PROMEDIO(C6:C1005)`
* *Criterio de Éxito:* La celda del promedio simulado debe mostrar un valor muy cercano a $4.00$ al iterar con la tecla **F9**.