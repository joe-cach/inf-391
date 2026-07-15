# Unidad 3: Variables Aleatorias Discretas (Parte 1)

**Enfoque:** Algoritmos matemáticos de números enteros para resolver la lógica de ruteo y los Rombos de Decisión en los diagramas de flujo.

> **Cita Académica Clave:** > Ross, S. M. (2012). *Simulation* (5ta ed.). Academic Press. 
> *(Capítulo 4: Generating Discrete Random Variables, que formaliza la arquitectura matemática para bifurcaciones lógicas).*

---

## El Rol de las Variables Discretas en la Arquitectura

En la simulación orientada a eventos, las **Variables Aleatorias Discretas** son aquellas que operan estrictamente con números enteros o categorías finitas. No admiten decimales ni fracciones. 

Si las variables continuas son el "reloj" del sistema, las variables discretas son el **"timón"**. Las utilizamos de manera exclusiva para programar los **Rombos de Decisión** en nuestros diagramas de flujo. Su trabajo algorítmico es recibir el número pseudoaleatorio crudo $U(0,1)$ y transformarlo en una elección física: *"¿La entidad toma el Camino A o el Camino B?"* o *"¿Qué tipo de cliente acaba de llegar?"*.

A continuación, presentamos el catálogo de distribuciones discretas esenciales para el ruteo lógico en ingeniería de software.

---

## 3.4. Catálogo de Variables Discretas (Ruteo Lógico)

### 3.4.1. Distribución de Bernoulli

**Definición:**
Es el algoritmo de decisión más fundamental de la estadística. Modela un experimento aislado que posee **exactamente dos salidas mutuamente excluyentes** (tradicionalmente denominadas "Éxito" y "Fracaso", o 1 y 0).

**Componentes Matemáticos:**
El sistema depende de un único parámetro configurado:
* **$p$ (Probabilidad de éxito):** Un valor decimal entre $0$ y $1$ que representa el peso histórico de la rama principal del rombo lógico.

**El Algoritmo de Ruteo:**
1. Generar $U \sim \text{Uniform}(0,1)$.
2. Si $U \le p \implies$ Retornar $1$ (Ejecutar Camino A).
3. Si $U > p \implies$ Retornar $0$ (Ejecutar Camino B).

**¿Para qué sirve en sistemas informáticos?**
Se aplica en cualquier nodo arquitectónico que funcione como un filtro o compuerta booleana. 
* *Ejemplos:* Un *firewall* decide si un paquete es válido ($p=0.99$) o malicioso. Una pasarela de pago decide si una transacción con tarjeta es aprobada o rechazada por el banco.

---

### 3.4.2. Distribución Empírica Discreta

**Definición:**
La distribución de Bernoulli es inútil cuando un rombo lógico tiene 3, 4 o más salidas posibles. En la vida real, los sistemas empresariales rara vez se comportan bajo fórmulas matemáticas perfectas; se comportan según el mercado. La Distribución Empírica permite construir una **tabla de ruteo personalizada** basada directamente en los datos históricos (la empiria) extraídos de la base de datos de producción.

**Componentes Matemáticos:**
* **$x_i$:** Los posibles caminos o categorías (ej. Plan Básico, Plan Pro, Plan Enterprise).
* **$p(x_i)$:** La probabilidad individual de cada camino. La suma total de todos los $p(x_i)$ debe ser obligatoriamente $1.00$.
* **$F(x)$ (Acumulada):** El apilamiento de los porcentajes desde $0$ hasta $1$ para crear "rangos" o "intervalos" de medición.

**El Algoritmo de Ruteo:**
1. Apilar las probabilidades históricas formando escalones.
2. Generar $U \sim \text{Uniform}(0,1)$.
3. Evaluar en qué "escalón" (rango) de $F(x)$ cae el valor de $U$.

**¿Para qué sirve en sistemas informáticos?**
Es la herramienta predilecta para la tipificación de entidades y el balanceo asimétrico.
* *Ejemplos:* Un *API Gateway* distribuyendo tráfico donde el 20% va al microservicio de Autenticación, el 50% al de Consultas y el 30% al de Mutaciones. En un autolavado, determinar si el vehículo entrante elegirá el lavado rápido, normal o VIP según el historial de ventas del mes pasado.

---

### 3.4.3. Distribución Uniforme Discreta

**Definición:**
Es el equivalente matemático a lanzar un dado perfecto de $N$ caras. Modela un escenario donde existen múltiples caminos disponibles, pero **absolutamente todos tienen la misma probabilidad de ser elegidos**. No existe sesgo histórico hacia ninguna opción.

**Componentes Matemáticos:**
* **$a$:** Límite inferior (generalmente el camino 1).
* **$b$:** Límite superior (generalmente el camino $N$).
* **Probabilidad:** Cada camino tiene una probabilidad exacta de $P(X=x) = \frac{1}{b - a + 1}$.

**El Algoritmo de Ruteo:**
La fórmula para transformar el generador base es:
$$X = a + \lfloor U \cdot (b - a + 1) \rfloor$$
*(Donde $\lfloor \dots \rfloor$ representa la operación de truncamiento o redondeo hacia abajo para asegurar un número entero).*

**¿Para qué sirve en sistemas informáticos?**
Se utiliza en sistemas de asignación "ciega" o arquitecturas distribuidas sin estado (*stateless*).
* *Ejemplos:* Un balanceador de carga puro tipo *Round-Robin* o aleatorio que debe repartir peticiones HTTP a un clúster de 4 servidores backend idénticos (cada servidor tiene exactamente un 25% de probabilidad de recibir el tráfico, sin importar su rendimiento actual).