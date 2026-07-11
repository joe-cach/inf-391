# Ejercicio Resuelto 1: Red de Petri Clásica (Modelo Productor-Consumidor)

## 1. El Escenario del Problema
Tenemos dos procesos informáticos paralelos: un **Productor** (ej. una cámara que captura fotos) y un **Consumidor** (ej. un algoritmo que comprime esas fotos). 
* El Productor genera un dato y lo deposita en un **Buffer** (memoria intermedia). 
* El Consumidor toma el dato del Buffer y lo procesa. 
* Para este ejercicio básico, asumiremos que el Buffer tiene capacidad infinita.

---

## 2. Descripción Formal (La Tupla Matemática)
Toda Red de Petri Clásica se define estrictamente mediante la tupla: 
$$PN = (P, T, F, W, M_0)$$

A continuación, extraemos cada componente del enunciado:

### A. Conjunto de Lugares ($P$)
Los lugares (círculos) representan el estado, las condiciones o los recursos disponibles.
$$P = \{p_1, p_2, p_3\}$$
* $p_1$: El Productor está listo para trabajar.
* $p_2$: El Buffer (contiene los elementos producidos).
* $p_3$: El Consumidor está listo para trabajar.

### B. Conjunto de Transiciones ($T$)
Las transiciones (rectángulos) representan las acciones o eventos que ocurren en el sistema.
$$T = \{t_1, t_2\}$$
* $t_1$: Acción de "Producir y Enviar al Buffer".
* $t_2$: Acción de "Extraer del Buffer y Consumir".

### C. Relación de Flujo ($F$) y Pesos ($W$)
Define cómo se conectan los nodos con arcos direccionales y cuántos tokens viajan por cada arco.
* Arco de $p_1 \to t_1$ (Peso $W=1$): El productor inicia la acción.
* Arco de $t_1 \to p_1$ (Peso $W=1$): El productor termina y vuelve a estar listo.
* Arco de $t_1 \to p_2$ (Peso $W=1$): La acción de producir genera 1 elemento en el buffer.
* Arco de $p_2 \to t_2$ (Peso $W=1$): La acción de consumir requiere 1 elemento del buffer.
* Arco de $p_3 \to t_2$ (Peso $W=1$): La acción de consumir requiere que el consumidor esté listo.
* Arco de $t_2 \to p_3$ (Peso $W=1$): El consumidor termina y vuelve a estar listo.

### D. Marcado Inicial ($M_0$)
El estado del sistema en el instante $t=0$. Se representa como un vector columna indicando la cantidad de tokens en cada lugar $[p_1, p_2, p_3]^T$.
$$M_0 = \begin{bmatrix} 1 \\ 0 \\ 1 \end{bmatrix}$$
*(Interpretación: Hay 1 Productor listo, 0 elementos en el Buffer, y 1 Consumidor listo).*



---

## 3. Resolución Analítica (Cálculo Matricial)
En papel, para evitar dibujar los tokens moviéndose uno por uno, traducimos el grafo a matrices. Esto es exactamente lo que hace el software internamente.

### Matriz de Incidencia Previa ($Pre$ o $I^-$)
Define cuántos tokens *necesita* extraer una transición de sus lugares de entrada. Las filas son Lugares ($P$) y las columnas Transiciones ($T$).
$$Pre = \begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 0 & 1 \end{bmatrix}$$
*(Ej. Para disparar $t_2$, miro la columna 2: necesito 0 tokens de $p_1$, 1 de $p_2$ y 1 de $p_3$).*

### Matriz de Incidencia Posterior ($Post$ o $I^+$)
Define cuántos tokens *deposita* una transición en sus lugares de salida.
$$Post = \begin{bmatrix} 1 & 0 \\ 1 & 0 \\ 0 & 1 \end{bmatrix}$$
*(Ej. Cuando se dispara $t_1$, miro la columna 1: deposita 1 token en $p_1$, 1 en $p_2$ y 0 en $p_3$).*

### Matriz de Incidencia ($D$)
Es el resumen algebraico de la red. Muestra el cambio neto de tokens. Se calcula como: $D = Post - Pre$.
$$D = \begin{bmatrix} 1 & 0 \\ 1 & 0 \\ 0 & 1 \end{bmatrix} - \begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 0 & 0 \\ 1 & -1 \\ 0 & 0 \end{bmatrix}$$
*(Análisis de la Matriz $D$: La primera fila ($p_1$) es puro 0, significa que el número de productores nunca cambia. La segunda fila ($p_2$) muestra que $t_1$ suma 1 elemento al buffer y $t_2$ le resta 1).*

---

## 4. Ecuación de Estado (Simulación Matemática)
Vamos a calcular matemáticamente qué pasa si el Productor dispara su evento ($t_1$).
El vector de disparo se define como $u = [1, 0]^T$ (se dispara $t_1$, no se dispara $t_2$).

La ecuación de estado es:
$$M_{k+1} = M_k + D \cdot u$$

Sustituyendo los valores:
$$M_1 = \begin{bmatrix} 1 \\ 0 \\ 1 \end{bmatrix} + \begin{bmatrix} 0 & 0 \\ 1 & -1 \\ 0 & 0 \end{bmatrix} \cdot \begin{bmatrix} 1 \\ 0 \end{bmatrix}$$

$$M_1 = \begin{bmatrix} 1 \\ 0 \\ 1 \end{bmatrix} + \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix} = \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix}$$

**Resultado Analítico:**
El nuevo marcado es $M_1 = [1, 1, 1]^T$. Esto significa matemáticamente que tras el disparo de $t_1$, el Productor sigue listo (1), hay un elemento disponible en el Buffer (1), y el Consumidor sigue listo (1). En este nuevo estado, la transición $t_2$ ya cuenta con los permisos matemáticos para dispararse.