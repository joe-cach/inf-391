# Unidad 3: Generación de Variables Aleatorias (Parte 2)

**Enfoque:** Métodos algorítmicos avanzados (fuerza bruta y composición) para generar variables aleatorias cuando el cálculo diferencial tradicional falla.

> **Cita Académica Clave:** > Von Neumann, J. (1951). *Various techniques used in connection with random digits*. National Bureau of Standards Applied Math Series.

---

## El Límite de la Transformada Inversa

En la Parte 1, establecimos que el Método de la Transformada Inversa ($X = F^{-1}(U)$) es el estándar de oro por su eficiencia de un solo paso computacional. Sin embargo, en la ingeniería de software nos encontramos con un muro matemático infranqueable: **¿Qué sucede si la función de densidad $f(x)$ es imposible de integrar analíticamente?**

El caso más famoso es la **Distribución Normal (Campana de Gauss)**. Su integral no tiene una solución cerrada exacta. Es imposible despejar algebraicamente la $X$. Ante este bloqueo del cálculo, se debe abandonar el álgebra lineal y recurrir a la algoritmia y a los ciclos de la CPU. 

Para estos casos, utilizamos dos métodos de rescate computacional.

---

## 3.4. Método de Aceptación-Rechazo (Von Neumann)

Inventado por John von Neumann durante el Proyecto Manhattan, este algoritmo cambia el enfoque matemático por un enfoque geométrico basado en el descarte iterativo. 

### El Fundamento Geométrico
Imagina que dibujamos la curva matemática compleja $f(x)$ (la que queremos simular) dentro de una caja rectangular (o debajo de otra curva más simple que sí sabemos calcular, llamada función mayorante $c \cdot g(x)$). 

El algoritmo genera coordenadas aleatorias $(X, Y)$ como si estuviera "lanzando dardos" a ciegas dentro de la caja. 
* Si el dardo cae **debajo** de nuestra curva $f(x)$, **Aceptamos** el valor de $X$ como un tiempo válido.
* Si el dardo cae **arriba** de la curva (en el espacio vacío de la caja), **Rechazamos** el valor, descartamos los números y repetimos el ciclo.

### El Algoritmo de Programación (Bucle `while`)
A diferencia de la transformada inversa que se ejecuta en $O(1)$, el método de aceptación-rechazo requiere un bucle condicional, consumiendo un número impredecible de ciclos de reloj de la CPU hasta lograr un "éxito".

1. **Paso 1:** Generar un número aleatorio crudo $U_1$. Transformarlo para obtener un valor candidato $X$ en el eje horizontal.
2. **Paso 2:** Generar un segundo número aleatorio crudo $U_2$ para simular el dardo en el eje vertical.
3. **Paso 3 (La Guarda Lógica):** Evaluar si el dardo cayó bajo la curva. Matemáticamente, comprobamos si:
   $$U_2 \le \frac{f(X)}{c \cdot g(X)}$$
4. **Paso 4:** * Si la condición es **Verdadera** $\implies$ Retornar $X$ (Fin del algoritmo).
   * Si la condición es **Falsa** $\implies$ Descartar $X$, volver al Paso 1 (Iterar el bucle `while`).

**¿Para qué sirve en sistemas?**
Es el "comodín" definitivo. Nos permite programar simuladores para curvas estadísticas altamente personalizadas o funciones caprichosas extraídas del aprendizaje automático (*Machine Learning*) donde no existe una fórmula estándar.

---

## 3.5. Método de Convolución

La convolución es el principio algorítmico de "divide y vencerás". En lugar de intentar programar una variable aleatoria matemática extremadamente compleja, analizamos si esa variable compleja es, en realidad, la suma de muchas variables simples.

### El Fundamento Lógico
Matemáticamente, la variable aleatoria compleja $X$ se puede expresar como la suma de $n$ variables aleatorias independientes $Y_i$:
$$X = Y_1 + Y_2 + Y_3 + \dots + Y_n$$

Si sabemos cómo generar la variable simple $Y$ (usando la Transformada Inversa de la Parte 1), no necesitamos descubrir la fórmula de $X$; simplemente generamos múltiples $Y$ en un bucle `for` y las sumamos.

### El Algoritmo de Programación
1. Iniciar un acumulador en cero: `X = 0`.
2. Iniciar un bucle `for` que itere $n$ veces.
3. Dentro del bucle, generar un $U(0,1)$ y usar la transformada inversa para obtener un valor $Y_i$.
4. Sumar el valor al acumulador: `X = X + Y_i`.
5. Al terminar el bucle, retornar $X$.

**¿Para qué sirve en sistemas?**
* **Tiempos de Pipeline (Distribución Erlang/Gamma):** Si tienes un proceso de datos en 5 etapas secuenciales, y cada etapa sigue un tiempo exponencial simple, el tiempo total es una Distribución de Erlang. En el código, simplemente generas 5 tiempos exponenciales y los sumas.
* **Fallos en Lotes (Distribución Binomial):** En lugar de usar una fórmula binomial compleja, puedes usar el método de convolución generando $n$ experimentos de Bernoulli (0 o 1) simples y sumando los resultados para saber cuántos paquetes de red fallaron en un lote de $n$ envíos.