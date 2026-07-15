# Unidad 3: Generación de Variables Aleatorias (Parte 1)

**Enfoque:** El determinismo informático, las limitaciones del hardware y el uso de algoritmos matemáticos como motores de incertidumbre en la arquitectura de software.

> **Cita Académica Clave:** > Knuth, D. E. (1997). *The Art of Computer Programming, Volume 2: Seminumerical Algorithms* (3ra ed.). Addison-Wesley.
> *(John von Neumann: "Cualquiera que considere métodos aritméticos para producir dígitos aleatorios está, por supuesto, en un estado de pecado").*

---

## El Conflicto Computacional: El Determinismo

Para diseñar arquitecturas orientadas a eventos y simuladores estocásticos, primero debemos aceptar una limitación fundamental de la ingeniería de hardware: **las computadoras son máquinas de estados estrictamente determinísticas**. 

La Unidad Central de Procesamiento (CPU) no posee libre albedrío ni capacidad para entender el azar. Si a un algoritmo determinístico se le proporcionan las mismas entradas (inputs) y el mismo estado de memoria, ejecutará exactamente las mismas instrucciones y devolverá siempre la misma salida (output). Dado que no podemos generar azar verdadero (*True Randomness*) sin hardware especializado que mida entropía física (como el ruido térmico), debemos recurrir a la matemática algorítmica para falsificarlo.

---

## 3.1. Generación de Números Pseudoaleatorios

Para inyectar el caos del mundo real en la memoria de un simulador, utilizamos algoritmos conocidos como **Generadores de Números Pseudoaleatorios (PRNG - Pseudo-Random Number Generators)**. Estos algoritmos producen secuencias de números que pasan rigurosas pruebas estadísticas de aleatoriedad, pero que están predeterminadas por una ecuación.

### La Semilla (Seed)
Todo PRNG necesita un estado inicial para arrancar la secuencia matemática. A este valor se le denomina **Semilla**. Si dos computadoras inicializan el mismo PRNG con la misma semilla, producirán exactamente la misma secuencia de millones de números. Esto es extremadamente útil en ingeniería de software para depurar (*debuggear*) modelos estocásticos y replicar escenarios de fallo exactos.

### La Materia Prima: $U(0,1)$
El objetivo exclusivo de los algoritmos PRNG (como el *Mersenne Twister* usado en la función `random()` de Python o `=ALEATORIO()` en Excel) es generar la distribución estadística base de la computación: la **Distribución Uniforme Continua entre 0 y 1**. 

En la notación matemática formal, la definimos como:
$$U \sim \text{Uniform}(0, 1)$$



**Propiedades fundamentales de $U(0,1)$ en el código:**
1. **Espectro Continuo:** Genera valores decimales con la máxima precisión de punto flotante que permita la arquitectura (ej. $0.419283741$).
2. **Límites:** El valor generado siempre satisface $0 \le U < 1$.
3. **Equiprobabilidad Estricta:** Ningún sub-rango tiene mayor preferencia. La probabilidad de que la computadora genere un número entre $0.1$ y $0.2$ es matemáticamente idéntica a la probabilidad de que lo genere entre $0.8$ y $0.9$. Su función de densidad es una constante: $f(x) = 1$.

Este número $U(0,1)$ es el combustible crudo. Sin embargo, un valor como $0.419$ no tiene ninguna semántica directa. No podemos decirle a un diagrama de flujo que "un proceso de base de datos tarda 0.419". Necesitamos transformarlo.

---

## 3.2. Generación de Variables Aleatorias

En este unto entra el concepto de **Moldeado Estadístico**. Una Variable Aleatoria es una abstracción matemática que toma la materia prima $U(0,1)$ y la "deforma", mapeando ese número sin sentido a un valor físico que nuestro diagrama de flujo y arquitectura puedan entender.

En el contexto de la simulación de sistemas discretos, moldeamos la incertidumbre en dos grandes familias:

* **Variables Aleatorias Discretas (La Lógica y el Ruteo):** Carecen de decimales. Se utilizan exclusivamente para programar los **Rombos de Decisión** en la arquitectura. Transforman a $U$ en una bifurcación lógica (ej. el flujo de red se va por la Rama A o la Rama B) o en un conteo de eventos finito.
* **Variables Aleatorias Continuas (La Cronometría y el Tiempo):** Poseen infinitos decimales. Se utilizan exclusivamente para programar los **Rectángulos de Proceso** (el estado de *Delay* o demora). Transforman a $U$ en un cronómetro físico que determina cuántos milisegundos debe bloquearse un hilo de ejecución.

---

## 3.3. Método de Generación Base: La Transformada Inversa

Para convertir matemáticamente el número uniforme $U(0,1)$ en una variable aleatoria continua $X$ (con comportamiento de campana de Gauss, decaimiento exponencial, etc.), el algoritmo más fundamental es el **Método de la Transformada Inversa**.



### El Fundamento Geométrico
Este algoritmo se basa en la Función de Distribución Acumulada (FDA), denotada como $F(x)$. Por definición estadística, el área acumulada de cualquier curva de probabilidad siempre crecerá desde $0$ hasta exactamente $1$. 

Casualmente, nuestro motor computacional genera números $U$ exactamente entre $0$ y $1$. Por lo tanto, podemos igualar nuestro número crudo al eje $Y$ de la gráfica acumulada, y leer el eje $X$ hacia atrás para obtener el tiempo físico.

### El Algoritmo de Programación (4 Pasos)
1. **Definir la Densidad:** Identificamos la curva de comportamiento del sistema, la Función de Densidad de Probabilidad, $f(x)$.
2. **Integrar al 100%:** Calculamos su función acumulada, $F(x)$, resolviendo la integral desde el límite inferior hasta la variable dependiente $x$: 
   $$F(x) = \int_{-\infty}^{x} f(t) dt$$
3. **Igualar al Motor:** Inyectamos el número pseudoaleatorio de nuestra computadora igualando la ecuación a $U$: 
   $$F(x) = U$$
4. **Despejar el Algoritmo:** Resolvemos el álgebra para despejar la variable $X$. El resultado es la función generadora inversa que escribiremos directamente en nuestro código fuente:
   $$X = F^{-1}(U)$$

*(Nota: En la Parte 2 exploraremos qué hacer cuando la integral del Paso 2 es imposible de resolver analíticamente y la Transformada Inversa falla).*