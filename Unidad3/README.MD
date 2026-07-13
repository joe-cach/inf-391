# Unidad 3: Generación de Variables Aleatorias
**Enfoque:** El motor estocástico de la simulación y la matemática detrás de la incertidumbre computacional.

---

## El Problema Fundamental del Azar
**El Concepto Clave:**
Hasta ahora hemos diseñado la estructura lógica del sistema (rutas, colas y servidores), pero nos falta un elemento crucial: **el tiempo**. En el mundo real, los clientes no llegan exactamente cada 5 minutos, ni los servidores tardan exactamente 10 segundos en procesar una petición. Existe variabilidad e incertidumbre.

Sin embargo, nos enfrentamos a un problema informático grave: **Las computadoras son máquinas estrictamente determinísticas**. No tienen voluntad ni pueden lanzar una moneda al aire. Si un código recibe las mismas entradas, siempre dará la misma salida. Entonces, ¿cómo programamos el "azar" dentro de una máquina que no sabe qué es el azar?

Esta unidad resuelve ese problema en cuatro etapas.

---

## 3.1. Generación de Números Pseudo Aleatorios
**Cita Académica:**
> L'Ecuyer, P. (1998). *Random Number Generation*. En *Handbook of Simulation*. John Wiley & Sons.

**¿Qué es?**
Es la creación de una secuencia de números mediante algoritmos matemáticos estrictos que, aunque son predecibles si conoces la "semilla" inicial, se comportan estadísticamente como si fueran completamente independientes y uniformes.

**Componentes:**
* **La Semilla (Seed):** El valor inicial que arranca la secuencia determinística.
* **El Generador Uniforme $U(0,1)$:** Algoritmos (como el *Mersenne Twister* o los Congruenciales Lineales) que escupen un valor decimal entre 0 y 1.

**¿Para qué sirve?**
Es el "combustible crudo" de nuestro simulador. Todo evento estocástico en nuestro código dependerá matemáticamente de generar primero un número $U(0,1)$ de alta calidad.

---

## 3.2. Generación de Variables Aleatorias
**Cita Académica:**
> Law, A. M. (2015). *Simulation Modeling and Analysis*. McGraw-Hill.

**¿Qué es?**
Un número crudo entre 0 y 1 no nos sirve para simular la realidad. No podemos decirle al cliente: *"Su paquete llegará en 0.732 horas"*. Necesitamos transformar ese número crudo en una **Variable Aleatoria** que siga una distribución estadística del mundo real (como la Normal, Exponencial o de Poisson).

**Componentes:**
* **Variables Discretas:** Representan conteos exactos (ej. número de paquetes defectuosos en un lote).
* **Variables Continuas:** Representan magnitudes físicas ininterrumpidas (ej. milisegundos de latencia en la red).

**¿Para qué sirve?**
Para traducir el azar computacional puro en métricas de comportamiento humano o de infraestructura.

---

## 3.3. Métodos de Generación
**Cita Académica:**
> Devroye, L. (1986). *Non-Uniform Random Variate Generation*. Springer-Verlag.

**¿Qué es?**
Son las técnicas algebraicas y algorítmicas que utilizamos para deformar la distribución uniforme $U(0,1)$ y obligarla a tomar la forma de la campana de Gauss, de una caída exponencial o de cualquier otra curva estadística que necesitemos.

**Métodos Clave:**
* **Método de la Transformada Inversa:** Utiliza la función acumulada inversa, matemáticamente definida como $X = F^{-1}(U)$.
* **Método de Aceptación-Rechazo (Von Neumann):** Un algoritmo geométrico que "lanza dardos" debajo de una curva para generar valores de funciones muy complejas.
* **Método de Convolución:** Suma de variables aleatorias más simples.

**¿Para qué sirve?**
Es la herramienta matemática para escribir en nuestro código fuente las funciones generadoras que escupirán los tiempos de llegada y de servicio.

---

## 3.4. Aplicación (Inyectando Incertidumbre al Modelo)
**Cita Académica:**
> Banks, J., Carson, J. S., Nelson, B. L., & Nicol, D. M. (2010). *Discrete-Event System Simulation*. Prentice Hall.

**¿Qué es?**
Es el acoplamiento final entre los algoritmos matemáticos de la Unidad 3 y los diagramas lógicos que construimos en la Unidad 2.

**Componentes:**
* **Generación de Tiempos de Llegada (Inter-arrival times).**
* **Generación de Tiempos de Servicio (Service times).**
* **Ruteo Probabilístico:** Usar azar para decidir qué camino toma una entidad en el diagrama de flujo (ej. 80% de los clientes pagan en efectivo, 20% con tarjeta).

**¿Para qué sirve?**
Es el momento en el que el simulador cobra vida. Sustituimos los valores fijos por nuestras nuevas funciones estocásticas, logrando que cada corrida del programa sea diferente, generando los escenarios de estrés que revelarán si el sistema soporta o colapsa.