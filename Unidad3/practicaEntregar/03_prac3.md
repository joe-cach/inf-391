# Práctica 3: Modelo Híbrido Estocástico (Continuas y Discretas)

**Escenario de Estudio:** API Gateway, Firewall (WAF) y Base de Datos.
**Objetivo:** Modelar el ciclo de vida de una petición HTTP inyectando múltiples variables aleatorias en serie, controlando tanto el ruteo lógico como los cuellos de botella temporales.

---

## 1. Identificación y Reglas de la Arquitectura

1. **Llegada:** Las peticiones HTTP llegan al API Gateway desde internet de manera asíncrona.
2. **Filtro de Seguridad (WAF):** Cada petición pasa por un *Web Application Firewall*. Si se detecta como tráfico malicioso (DDoS/Bot), se descarta inmediatamente (*Drop*) y no consume más recursos. Si es legítima, avanza.
3. **Ruteo de Base de Datos:** Las peticiones válidas se enrutan hacia el motor de base de datos. Pueden ser consultas de solo lectura (`SELECT`) o de escritura (`INSERT/UPDATE`).
4. **Ejecución (Demora):** La base de datos procesa la consulta y bloquea el hilo de ejecución durante un tiempo específico antes de retornar el *Status 200 OK*.

---

## 2. Modelado Matemático (Input Modeling)

Para este sistema, el ingeniero ha parametrizado 4 variables aleatorias (2 Continuas y 2 Discretas):

*   **Continua 1: Llegadas de Red (Exponencial)**
    *   *Física:* Cronómetro entre la llegada de una petición y otra.
    *   *Parámetro:* Promedio de $\beta = 10$ ms.
    *   *Fórmula:* $T_{llegada} = -10 \cdot \ln(1 - U)$
*   **Discreta 1: Seguridad WAF (Bernoulli)**
    *   *Física:* Decisión binaria. Históricamente el 80% es tráfico legítimo, el 20% es malicioso.
    *   *Lógica:* Si $U \le 0.80 \implies$ "Legítimo". Caso contrario $\implies$ "Bloqueado".
*   **Discreta 2: Tipo de Consulta (Empírica)**
    *   *Física:* Bifurcación. El 70% son operaciones de lectura (`SELECT`), el 30% de escritura (`UPDATE`).
    *   *Lógica:* Si $U \le 0.70 \implies$ "SELECT". Caso contrario $\implies$ "UPDATE".
*   **Continua 2: Tiempo de Procesamiento BD (Uniforme Continua)**
    *   *Física:* Demora del hardware del servidor. Oscila de manera constante entre $15$ ms y $25$ ms, sin importar el tipo de consulta.
    *   *Parámetros:* $a = 15$, $b = 25$.
    *   *Fórmula:* $T_{bd} = 15 + U \cdot (25 - 15) = 15 + 10U$

---

## 3. Prueba de Escritorio (Traza Manual)

Asumimos que el motor generó la siguiente cinta de números en la memoria RAM: `[0.35, 0.75, 0.45, 0.90, 0.15, 0.85]`

### Procesamiento de la Petición 1
*   **Paso 1 (Llegada - C1):** Consume $U = 0.35$.
    *   $T = -10 \cdot \ln(1 - 0.35) = -10 \cdot \ln(0.65) \approx \mathbf{4.31 \text{ ms}}$. *(El reloj marca 4.31 ms).*
*   **Paso 2 (Seguridad - D1):** Consume $U = 0.75$.
    *   Evaluación: $0.75 \le 0.80 \implies$ **Legítimo**. (Avanza).
*   **Paso 3 (Ruteo - D2):** Consume $U = 0.45$.
    *   Evaluación: $0.45 \le 0.70 \implies$ **Consulta SELECT**.
*   **Paso 4 (Ejecución BD - C2):** Consume $U = 0.90$.
    *   Demora: $T_{bd} = 15 + 10(0.90) = 15 + 9 = \mathbf{24.00 \text{ ms}}$.
*   *Resultado Final Petición 1:* Ingresó al sistema en el ms 4.31, fue aceptada, hizo un SELECT y la base de datos la liberó en el ms absoluto $4.31 + 24.00 = \mathbf{28.31 \text{ ms}}$.

### Procesamiento de la Petición 2
*   **Paso 1 (Llegada - C1):** Consume $U = 0.15$.
    *   $T = -10 \cdot \ln(1 - 0.15) \approx \mathbf{1.62 \text{ ms}}$. 
    *   *(El reloj avanza desde la llegada anterior: $4.31 + 1.62 = \mathbf{5.93 \text{ ms}}$).*
*   **Paso 2 (Seguridad - D1):** Consume $U = 0.85$.
    *   Evaluación: $0.85 > 0.80 \implies$ **Bloqueado (Ataque)**.
*   *Resultado Final Petición 2:* El cortafuegos destruye la petición en el ms 5.93. No consume recursos de base de datos ni más números aleatorios.

---

## 4. Laboratorio Computacional en Excel

En este laboratorio anidaremos las 4 ecuaciones. Es vital usar múltiples motores $U(0,1)$ para evitar que las variables se contaminen entre sí (un error gravísimo llamado "correlación inducida").

### A. Panel de Control (Cabecera)
*   **Llegadas:** `B1` = 10 (Beta Promedio).
*   **WAF:** `B2` = 0.80 (Probabilidad Legítimo).
*   **BD Tipo:** `B3` = 0.70 (Probabilidad SELECT).
*   **Hardware Mín:** `B4` = 15 | **Hardware Máx:** `B5` = 25.

### B. Matriz de Simulación (A partir de la Fila 8)
Construiremos una fila por cada petición HTTP (1000 filas). Cada decisión independiente requiere su propia columna de motor aleatorio.

*   **A (ID_Req):** 1 a 1000.
*   **B (U_Llegada):** `=ALEATORIO()`
*   **C (Tiempo Llegada ms):** `=-$B$1 * LN(1 - B8)`
*   **D (U_WAF):** `=ALEATORIO()`
*   **E (Estado Firewall):** `=SI(D8 <= $B$2; "Legítimo"; "Bloqueado")`
*   **F (U_Query):** `=ALEATORIO()`
*   **G (Tipo de Query):** `=SI(E8="Bloqueado"; "N/A"; SI(F8 <= $B$3; "SELECT"; "UPDATE"))`
    *(Nota: Usamos lógica de software. Si fue bloqueado, no hay query).*
*   **H (U_Hardware):** `=ALEATORIO()`
*   **I (Demora BD ms):** `=SI(E8="Bloqueado"; 0; $B$4 + H8 * ($B$5 - $B$4))`
    *(Si fue bloqueado, la demora de base de datos es 0 ms, liberando el hilo).*

### C. Validación y Análisis (Auditoría)
El estudiante debe comprobar estadísticamente toda la cadena usando las 1000 filas:

1.  **Media de Llegadas (C1):** `=PROMEDIO(C8:C1007)` $\rightarrow$ Debe orbitar los 10 ms.
2.  **Tasa de Tráfico Limpio (D1):** `=CONTAR.SI(E8:E1007; "Legítimo") / 1000` $\rightarrow$ Debe orbitar el 80%.
3.  **Porcentaje de SELECTS (D2):** `=CONTAR.SI(G8:G1007; "SELECT") / CONTAR.SI(G8:G1007; "<>N/A")` $\rightarrow$ Debe orbitar el 70% respecto al tráfico limpio.
4.  **Carga Promedio de CPU (C2):** `=PROMEDIO.SI(I8:I1007; ">0")` $\rightarrow$ Evaluando solo los tiempos mayores a 0 (peticiones no bloqueadas), el promedio debe ser $\frac{15+25}{2} = 20.00$ ms.