# Unidad 3: Variables Aleatorias Continuas (Parte 2)

**Enfoque:** Algoritmos matemáticos avanzados para calcular escenarios de estrés, desgaste de hardware, cuellos de botella en redes y la parametrización de sistemas cuando no existen bases de datos históricas.

> **Cita Académica Clave:** > Law, A. M. (2015). *Simulation Modeling and Analysis* (5ta ed.). McGraw-Hill Education. 
> *(Capítulo 6: Selección de distribuciones cuando los datos empíricos son inexistentes y modelado del tiempo hasta el fallo).*

---

## El Límite de las Distribuciones Estándar

En la Parte 1 analizamos las distribuciones continuas "ideales" (Exponencial, Normal, Uniforme). Sin embargo, cuando un arquitecto de software simula sistemas críticos, se enfrenta a dos realidades operativas graves:
1. **El Problema de la Ignorancia (Falta de Datos):** ¿Cómo programas el tiempo de demora de un microservicio si el sistema aún no ha sido construido y no tienes logs en la base de datos?
2. **El Problema del Desgaste (Confiabilidad):** Los servidores físicos no fallan de manera "normal" ni "exponencial"; fallan por desgaste acumulado a lo largo del tiempo. 

Para resolver estas lagunas en el modelado de entrada (*Input Modeling*), utilizamos distribuciones continuas avanzadas.

---

## 3.5. Catálogo de Variables Continuas (Casos Avanzados)

### 3.5.4. Distribución Triangular

**Definición:**
Es la herramienta de "rescate". Se utiliza exclusivamente cuando **no existen datos históricos** para construir una distribución empírica. En su lugar, recurrimos al juicio de un Experto en la Materia (SME - *Subject Matter Expert*), quien nos proporciona una estimación de tres puntos. La curva geométrica forma un triángulo exacto.

**Componentes Matemáticos (Los 3 Puntos):**
* **$a$:** El tiempo Mínimo u optimista (si todo sale perfecto).
* **$c$:** El tiempo Más Probable o la Moda (lo que suele ocurrir).
* **$b$:** El tiempo Máximo o pesimista (si ocurre un desastre o bloqueo).

**El Algoritmo de Generación (Transformada Inversa por Tramos):**
Debido a la forma de techo a dos aguas, el algoritmo evalúa en qué lado del triángulo cae el motor estocástico $U(0,1)$ mediante una condicional `if/else`:

Si $U \le \frac{c-a}{b-a}$:
$$X = a + \sqrt{U \cdot (b-a)(c-a)}$$
De lo contrario:
$$X = b - \sqrt{(1-U)(b-a)(b-c)}$$

**¿Para qué sirve en sistemas informáticos?**
Es indispensable en simulaciones de **Gestión de Proyectos de Software** y estimaciones ágiles.
* *Ejemplos:* Estimar cuánto tardará un programador *Senior* en compilar un nuevo módulo: $a = 2$ horas, $c = 5$ horas, $b = 14$ horas (si hay problemas de dependencias).

---

### 3.5.5. Distribución Lognormal

**Definición:**
Modela magnitudes físicas que jamás pueden ser negativas (el tiempo no va hacia atrás). Su característica principal es que agrupa la mayoría de los eventos en tiempos muy cortos y rápidos, pero posee una **"cola larga" (*Long Tail*) hacia la derecha**, lo que significa que de vez en cuando permite la generación de un tiempo extremadamente alto (un valor atípico o *outlier* severo).

**Componentes Matemáticos:**
* **$\mu$:** La media del logaritmo natural.
* **$\sigma$:** La desviación estándar del logaritmo natural.

**El Algoritmo de Generación:**
No se usa la Transformada Inversa directa. Se utiliza la propiedad matemática de que si el logaritmo de una variable es Normal, la variable en sí es Lognormal.
1. Generar una variable Normal estándar ($Y$) usando Box-Muller (Ver Parte 1).
2. Exponenciar el resultado: 
   $$X = e^Y$$

**¿Para qué sirve en sistemas informáticos?**
Es el estándar de oro para modelar la **Latencia de Red** y cuellos de botella en Internet.
* *Ejemplos:* El tiempo de descarga de un archivo de 1GB. El 99% de las veces la descarga es rápida (cae en la parte alta de la curva), pero si el canal TCP se congestiona o hay pérdida de paquetes, el tiempo se dispara hacia el infinito (la cola larga).

---

### 3.5.6. Distribución de Weibull

**Definición:**
Es el pilar de la **Ingeniería de Confiabilidad (*Reliability Engineering*)**. Mientras que la Exponencial asume que un sistema tiene la misma probabilidad de fallar hoy que dentro de 10 años, la distribución de Weibull modela **Tasas de Fallo que cambian con el tiempo**. Puede simular la "Mortalidad Infantil" (hardware que falla ni bien se enciende por defecto de fábrica) o el "Desgaste" (hardware que falla por vejez).

**Componentes Matemáticos:**
* **$\alpha$ (Parámetro de Forma):** Dicta el comportamiento físico. Si $\alpha < 1$ (falla al inicio), si $\alpha = 1$ (falla aleatoria), si $\alpha > 1$ (falla por desgaste de vejez).
* **$\beta$ (Parámetro de Escala):** La vida característica del sistema.

**El Algoritmo de Generación (Transformada Inversa):**
Afortunadamente, su función acumulada es invertible algebraicamente con extrema elegancia:
$$X = \beta \cdot (-\ln(1 - U))^{\frac{1}{\alpha}}$$

**¿Para qué sirve en sistemas informáticos?**
Se utiliza para programar los **Eventos de Caída Catastrófica** (*System Failures*) en simuladores de infraestructura.
* *Ejemplos:* Calcular el tiempo exacto (en horas operativas) antes de que un clúster de Memoria RAM sufra un *Kernel Panic* físico, o el Tiempo Medio Hasta el Fallo (MTTF) de un Disco de Estado Sólido (SSD) en un centro de datos.

---

### 3.5.7. Distribución Gamma

**Definición:**
Representa el tiempo total necesario para completar $k$ tareas secuenciales, asumiendo que cada una de esas tareas sigue una distribución exponencial independiente.

**Componentes Matemáticos:**
* **$k$ o $\alpha$ (Forma):** El número entero de sub-tareas o etapas en el sistema.
* **$\theta$ o $\beta$ (Escala):** El tiempo medio de cada etapa.

**El Algoritmo de Generación (Convolución):**
Cuando $k$ es un número entero (conocido como variante de Erlang), la generación más óptima en la CPU es un bucle que sume variables exponenciales:
1. Iniciar $X = 0$.
2. Iniciar un bucle de $1$ hasta $k$.
3. Generar $U \sim \text{Uniform}(0,1)$.
4. Calcular el tiempo de esa etapa: $t = -\beta \ln(1 - U)$.
5. $X = X + t$.
6. Al finalizar el bucle, retornar $X$ (Tiempo Total).

**¿Para qué sirve en sistemas informáticos?**
Es el modelo matemático perfecto para simular **Pipelines de Datos** y arquitecturas en serie.
* *Ejemplos:* Un proceso ETL (*Extract, Transform, Load*) en una base de datos. El proceso total (Gamma) no termina hasta que el hilo de ejecución pase por la Extracción (Exponencial 1), la Transformación (Exponencial 2) y la Carga (Exponencial 3).