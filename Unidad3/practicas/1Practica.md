# Unidad 3: Laboratorio Computacional - Variables Discretas en Excel

**Enfoque:** Transición de las pruebas manuales a la simulación estática masiva utilizando hojas de cálculo, aplicando las mejores prácticas de modelado financiero e ingeniería.

> **Cita Académica Clave:** > Winston, W. L. (2014). *Data Analysis and Decision Making* (5ta ed.). Cengage Learning. 
> *(El autor establece que un modelo estocástico en Excel debe separar estrictamente los parámetros estáticos del motor generador para garantizar su auditabilidad).*

---

## 1. La Metodología Experta para Simulaciones en Excel

Para que un modelo en Excel tenga rigor de ingeniería y no sea una simple hoja de cálculos desordenada, aplicaremos las "Tres Reglas de Oro" de la simulación en hojas de cálculo:

1. **Aislamiento de Parámetros:** Nunca se escribe un valor fijo (como $p = 0.85$) dentro de una fórmula. Los parámetros del sistema deben ir en un "Panel de Control" en la parte superior.
2. **La Columna de la Verdad $U(0,1)$:** Nunca se esconde la función `=ALEATORIO()` dentro de un `SI()`. Siempre debe existir una columna exclusiva y visible que genere el número crudo. Esto permite hacer *debug* manual.
3. **La Ley de los Grandes Números (La Prueba):** El azar individual es impredecible, pero el azar masivo es matemáticamente predecible. Para probar que nuestro modelo funciona, siempre debemos simular al menos $1,000$ filas y calcular los promedios globales para ver si coinciden con los parámetros iniciales.

---

## 2. Práctica 1: Distribución de Bernoulli (Filtro Binario)

**El Escenario:**
Modelaremos el *Firewall* de nuestro servidor. Los datos históricos indican que el 85% de los paquetes son legítimos ($p = 0.85$) y el 15% son ataques o paquetes corruptos.

### Paso 1: El Panel de Control
En las primeras celdas (ej. `A1:B2`), definimos nuestras variables estáticas:
* `A1`: **Probabilidad Éxito (p)** | `B1`: **0.85**
* `A2`: **Mensaje Éxito** | `B2`: **Válido**
* `A3`: **Mensaje Fracaso** | `B3`: **Corrupto**

### Paso 2: La Matriz de Simulación
A partir de la fila 5, creamos los encabezados para simular 1,000 paquetes:
* **Columna A (ID):** 1, 2, 3... hasta 1000.
* **Columna B (Motor U):** `=ALEATORIO()`
* **Columna C (Decisión Lógica):** Aplicamos la regla $U \le p$.
  * *Fórmula:* `=SI(B5 <= $B$1; $B$2; $B$3)`
  * *(Nota: Usamos el signo `$` para fijar el Panel de Control al arrastrar la fórmula hacia abajo).*

### Paso 3: La Prueba de Corrección (Verificación)
¿Cómo demostramos algorítmicamente que la simulación es correcta? Construimos un bloque de "Auditoría" al lado de nuestro panel de control.

Si programamos que $p = 0.85$, al simular 1,000 paquetes, aproximadamente 850 deberían ser válidos. Calculamos la **Frecuencia Empírica**:

1. **Total de Paquetes Simulados:** `=CONTARA(C5:C1004)`
2. **Total de Paquetes Válidos:** `=CONTAR.SI(C5:C1004; "Válido")`
3. **Probabilidad Simulada:** `=Total_Válidos / Total_Simulados`

*El estudiante debe presionar la tecla **F9** (Recalcular) varias veces. Verá que la "Probabilidad Simulada" fluctuará (ej. 0.842, 0.856, 0.839), pero siempre orbitará estrechamente alrededor del parámetro teórico $0.85$. Esta es la prueba absoluta de que el algoritmo está bien programado.*

---

## 3. Práctica 2: Distribución Empírica (Ruteo Múltiple)

**El Escenario:**
Modelaremos el *API Gateway* que enruta el tráfico HTTP a tres microservicios: Auth (20%), Query (50%) y Write (30%).

En Excel, no se recomienda usar la función `=SI()` anidada cuando hay más de 2 opciones, porque es ilegible. La práctica experta exige utilizar tablas de búsqueda con la función `=BUSCARV()` activada en modo de "coincidencia aproximada".

### Paso 1: La Tabla de Rangos (Panel de Control)
Debemos construir matemáticamente la Función Acumulada $F(x)$. Excel necesita que el límite inferior de cada rango esté explícito en una columna.

| Rango Acumulado (Límite Inferior) | Servicio Destino | Probabilidad Teórica |
| :--- | :--- | :--- |
| **0.00** | Auth | 20% |
| **0.20** | Query | 50% |
| **0.70** | Write | 30% |

*(Asumamos que esta tabla está en el rango `F2:G4`).*

### Paso 2: La Matriz de Simulación
* **Columna A (ID_Petición):** 1 a 1000.
* **Columna B (Motor U):** `=ALEATORIO()`
* **Columna C (Ruteo Físico):** * *Fórmula:* `=BUSCARV(B5; $F$2:$G$4; 2; VERDADERO)`
  * *Lógica:* La función lee el número crudo (ej. $0.65$), busca en la tabla de rangos, descubre que es mayor a $0.20$ pero no alcanza el $0.70$, y extrae la palabra "Query".

### Paso 3: La Prueba de Corrección (Verificación)
Para auditar que el balanceador de carga virtual funciona:
1. Calculamos las apariciones de cada servicio en la columna C: 
   `=CONTAR.SI(C5:C1004; "Query") / 1000`
2. El resultado debe oscilar muy cerca del $0.50$ (50%).
3. **Gráfico de Validación:** El profesor solicitará a los alumnos que inserten un Gráfico de Barras comparando los "Porcentajes Teóricos" vs "Porcentajes Simulados". Al presionar F9, las barras simuladas bailarán sutilmente, pero siempre mantendrán la estructura de la escalera original.