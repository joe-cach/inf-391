# Presentación 1: Fundamentación de las Variables Aleatorias
**Enfoque:** La base matemática de la incertidumbre computacional.

**Cita Académica:**
> Law, A. M. (2015). *Simulation Modeling and Analysis*. McGraw-Hill.
> *"Un modelo de simulación sin datos de entrada probabilísticos válidos es simplemente un ejercicio de programación estática, incapaz de predecir el comportamiento del sistema bajo estrés real."*

**¿Qué es? / Definición o Concepto:**
Una Variable Aleatoria (VA) es una regla matemática (una función) que asigna un valor numérico a cada resultado posible de un experimento impredecible. En programación, es la función que reemplaza los "tiempos fijos" (ej. `sleep(5)`) por tiempos dinámicos que imitan el caos del mundo real.



**Componentes:**
* **El Generador Base:** Un número pseudoaleatorio uniforme $U(0,1)$ producido por el motor informático.
* **La Función de Transformación:** El algoritmo matemático que deforma ese número $U$ para que se ajuste a una curva de probabilidad específica (la Variable Aleatoria real).

**¿Para qué sirve?:**
Sirve para alimentar de datos el Diagrama de Flujo que hicimos en la Unidad 2. Sin variables aleatorias, todos los clientes llegarían al mismo tiempo y todas las descargas de red tardarían los mismos segundos, lo cual es falso en la realidad.

---

# Presentación 2: Variaciones Discretas (Cantidades y Conteos)
**Enfoque:** Sucesos contables, finitos y eventos aislados en sistemas informáticos.

**Cita Académica:**
> Ross, S. M. (2012). *Simulation*. Academic Press.

**¿Qué es? / Definición o Concepto:**
Son variables aleatorias que solo pueden tomar valores enteros o saltos definidos (0, 1, 2, 3...). No existen fracciones. Se utilizan para modelar la "cantidad" de veces que ocurre un evento, no el tiempo que dura.

**Componentes (Distribuciones Clásicas):**
* **Distribución de Poisson:** Modela la cantidad de eventos que ocurren en una ventana de tiempo (ej. número de *logins* por minuto en un servidor).
* **Distribución Binomial:** Modela el número de "éxitos" en una secuencia de intentos (ej. cuántos paquetes TCP llegan corruptos de un lote de 100).
* **Distribución Empírica Discreta:** Creada directamente con datos históricos del cliente cuando ninguna fórmula matemática encaja (ej. 10% compra el plan Básico, 60% el Medio, 30% el Premium).

**¿Para qué sirve?:**
Para modelar atributos de estado exactos, tamaños de lotes de memoria, ruteo de decisiones (rombo del diagrama de flujo) o fallas de hardware.

**Ejemplos:**
* El número de discos duros que fallarán en un *Data Center* este mes.
* El número de consultas simultáneas que golpean la base de datos a las 10:00 AM.

---

# Presentación 3: Variaciones Continuas (El Factor del Tiempo)
**Enfoque:** Magnitudes ininterrumpidas, cronometría y demoras de procesamiento.

**Cita Académica:**
> Banks, J., Carson, J. S., Nelson, B. L., & Nicol, D. M. (2010). *Discrete-Event System Simulation*. Prentice Hall.

**¿Qué es? / Definición o Concepto:**
Son variables aleatorias que pueden tomar cualquier valor numérico dentro de un intervalo, incluyendo infinitos decimales. Son las dueñas absolutas del reloj del simulador.

**Componentes (Distribuciones Clásicas):**
* **Distribución Exponencial:** Modela el tiempo transcurrido *entre* dos eventos sucesivos. Tiene una propiedad de "falta de memoria" (ej. el tiempo exacto que pasa entre la llegada de un cliente HTTP y el siguiente).
* **Distribución Normal (Campana de Gauss):** Modela procesos que son la suma de muchos pequeños factores o errores (ej. el desgaste térmico de una CPU).
* **Distribución Uniforme Continua:** Modela eventos donde todos los tiempos tienen exactamente la misma probabilidad de ocurrir (usada generalmente cuando hay ignorancia total del sistema).

**¿Para qué sirve?:**
Es indispensable para calcular el estado *Delay* (Demora) en el motor de simulación. Nos dice exactamente cuántos milisegundos retener una entidad dentro de un servidor.

**Ejemplos:**
* El tiempo (en segundos y milisegundos) que tarda un algoritmo criptográfico en encriptar una contraseña.
* El tiempo exacto de latencia de un *ping* entre La Paz y un servidor en AWS.

---

# Presentación 4: El Método de la Transformada Inversa
**Enfoque:** El algoritmo fundamental de generación computacional.

**Cita Académica:**
> Devroye, L. (1986). *Non-Uniform Random Variate Generation*. Springer-Verlag.
> *(Considerada la "Biblia" matemática de la generación de distribuciones informáticas).*

**¿Qué es? / Definición o Concepto:**
Es el método matemático más directo y elegante para convertir un número aleatorio crudo $U(0,1)$ de la computadora en un valor de una distribución continua (como la Exponencial). 



**Componentes:**
1. **$f(x)$:** La Función de Densidad (la curva visual del problema).
2. **$F(x)$:** La Función Acumulada (la integración matemática de la curva, que siempre va de 0 a 1).
3. **$F^{-1}(U)$:** La Función Inversa. El algoritmo despeja matemáticamente la variable $X$, introduciendo el número aleatorio de la computadora ($U$) para obtener el tiempo físico simulado.

**¿Para qué sirve?:**
Para programar nuestras propias librerías estadísticas en lenguajes que no las traen por defecto. Si sabemos integrar la curva matemática del problema y despejar la $X$, podemos simular cualquier comportamiento físico.

**Ejemplos:**
El código en Python para generar el tiempo de llegada de un cliente no usa magia, usa la ecuación despejada de la transformada inversa exponencial: `tiempo = -beta * math.log(1 - U)`.

---

# Presentación 5: Variaciones de Métodos (Aceptación/Rechazo y Convolución)
**Enfoque:** Algoritmos de rescate cuando la matemática se rompe.

**Cita Académica:**
> Von Neumann, J. (1951). *Various techniques used in connection with random digits*. National Bureau of Standards Applied Math Series.

**¿Qué es? / Definición o Concepto:**
¿Qué pasa si la fórmula matemática del comportamiento de un servidor es tan compleja que es imposible despejar la variable $X$ (como ocurre con la Distribución Normal o Gamma)? La Transformada Inversa falla. Aquí entran las variaciones algorítmicas de rescate.

**Componentes:**
* **Método de Aceptación-Rechazo (Von Neumann):** Es un algoritmo geométrico. En lugar de resolver ecuaciones, encierra la curva difícil dentro de un rectángulo. La computadora genera coordenadas al azar $(X, Y)$ como si lanzara dardos; si el dardo cae bajo la curva, se "Acepta" como un tiempo válido; si cae fuera, se "Rechaza" y se itera el bucle `while`.
* **Método de Convolución:** Se basa en sumar cosas simples. Si quiero simular un proceso Gamma complicado, matemáticamente puedo simplemente generar y sumar varias exponenciales simples.

**¿Para qué sirve?:**
Para garantizar que el motor de simulación no tenga limitaciones matemáticas. Le da al ingeniero de software una salida algorítmica para modelar fenómenos extremadamente complejos donde el cálculo diferencial tradicional no es suficiente.