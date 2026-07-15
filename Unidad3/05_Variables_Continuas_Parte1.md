# Unidad 3: Variables Aleatorias Continuas (Parte 1)

**Enfoque:** Algoritmos matemáticos de magnitudes ininterrumpidas (con infinitos decimales) para calcular el tiempo cronológico y los Rectángulos de Proceso en la simulación de software y operaciones humanas.

> **Cita Académica Clave:** > Banks, J., Carson, J. S., Nelson, B. L., & Nicol, D. M. (2010). *Discrete-Event System Simulation* (5ta ed.). Prentice Hall. 
> *(Capítulo 5: Statistical Models in Simulation, que define los estándares para la cronometría de sistemas).*

---

## El Rol de las Variables Continuas en la Arquitectura

Si las variables discretas (Parte 1 y 2) funcionan como el "timón" que enruta las decisiones lógicas, las **Variables Aleatorias Continuas** son el **"Reloj"** de nuestro simulador. 

En la ingeniería de sistemas, el tiempo rara vez es un número entero exacto. Un proceso no tarda "5 segundos"; tarda $5.10293$ segundos. Las variables continuas operan en el espectro de los números reales, permitiendo infinitos decimales. Se utilizan de manera exclusiva para programar los **Rectángulos de Proceso** en nuestro diagrama de flujo, determinando exactamente cuántos milisegundos debe durar un estado de Demora (*Delay*) o calculando el tiempo exacto que transcurre antes de que el siguiente evento ingrese al sistema.

A continuación, presentamos el catálogo de distribuciones continuas estándar, utilizadas para modelar el comportamiento general del software y de los operadores humanos.

---

## 3.5. Catálogo de Variables Continuas (Tiempos Estándar)

### 3.5.1. Distribución Exponencial

**Definición:**
Es el rey indiscutible de los modelos de simulación. Modela el tiempo continuo que transcurre *entre* la ocurrencia de dos eventos asíncronos totalmente independientes. Su característica matemática más importante es la "falta de memoria": el hecho de que haya pasado mucho tiempo sin que llegue una petición al servidor no hace que sea más probable que llegue en el siguiente segundo.

**Componentes Matemáticos:**
* **$\beta$ (Tiempo promedio):** El tiempo medio histórico entre eventos (ej. "los clientes llegan en promedio cada 10 minutos"). En algunos textos se utiliza la tasa de llegada $\lambda$, donde $\beta = \frac{1}{\lambda}$.

**El Algoritmo de Generación (Transformada Inversa):**
Gracias a que la curva exponencial es fácilmente integrable, su función generadora se despeja analíticamente en una sola línea de código limpia y eficiente:
$$X = -\beta \ln(1 - U)$$

**¿Para qué sirve en sistemas informáticos?**
Es el estándar absoluto para generar la agilidad de los **Tiempos de Llegada** (*Inter-arrival times*).
* *Ejemplos:* Calcular en qué milisegundo exacto llegará la próxima petición HTTP al balanceador de carga. Determinar el tiempo entre la llegada de un vehículo y el siguiente a la puerta del autolavado.

---

### 3.5.2. Distribución Uniforme Continua

**Definición:**
Modela un espectro de tiempo cerrado donde **absolutamente cualquier milisegundo dentro del rango tiene la misma probabilidad de ocurrir**. No hay una tendencia hacia un valor central; la gráfica de su función de densidad es un rectángulo perfecto.

**Componentes Matemáticos:**
* **$a$:** Límite de tiempo inferior (Mínimo).
* **$b$:** Límite de tiempo superior (Máximo).

**El Algoritmo de Generación (Transformada Inversa):**
La inyección de nuestro motor base $U(0,1)$ escala el número entre los límites configurados mediante interpolación lineal:
$$X = a + U \cdot (b - a)$$

**¿Para qué sirve en sistemas informáticos?**
Se utiliza casi exclusivamente para modelar **Hardware Automatizado** o sistemas mecánicos con variaciones de desgaste muy pequeñas, así como sistemas en los que declaramos "ignorancia total" de la tendencia temporal.
* *Ejemplos:* Un brazo robótico en una línea de ensamblaje que siempre ejecuta un movimiento entre $4.1$ y $4.3$ segundos. El tiempo de lectura/escritura física de un bloque de datos en un disco duro mecánico.

---

### 3.5.3. Distribución Normal (Gaussiana)

**Definición:**
Es la famosa "Campana de Gauss". Modela tiempos de proceso que tienden fuertemente hacia un valor central (promedio), donde las desviaciones extremas (hacerlo muy rápido o muy lento) son extremadamente raras y simétricas. Físicamente, ocurre cuando el tiempo total es el resultado de la suma de muchas pequeñas variaciones independientes (Teorema del Límite Central).

**Componentes Matemáticos:**
* **$\mu$ (Media):** El tiempo central o promedio histórico.
* **$\sigma$ (Desviación Estándar):** La medida de qué tan ancha es la campana (qué tanto varía el tiempo respecto a la media).

**El Algoritmo de Generación (Box-Muller):**
Como la integral de la campana de Gauss no tiene una solución analítica cerrada (falla la Transformada Inversa simple), los informáticos utilizan el algoritmo de Box-Muller, que consume dos números uniformes para generar dos tiempos normales estandarizados ($Z_0$ y $Z_1$) mediante coordenadas polares:
$$Z_0 = \sqrt{-2 \ln(U_1)} \cos(2\pi U_2)$$
$$X = \mu + \sigma \cdot Z_0$$

**¿Para qué sirve en sistemas informáticos?**
Se utiliza para modelar los tiempos de procesamiento de **Operadores Humanos** y fenómenos biológicos.
* *Ejemplos:* El tiempo exacto que tarda un operador de *Call Center* en registrar manualmente los datos de un cliente en el CRM. El tiempo que le toma a un cajero físico contar billetes y sellar un depósito bancario. 
*(Nota arquitectónica: La distribución Normal matemáticamente puede generar valores negativos, lo cual es imposible para el tiempo físico. En simulación, si $\mu$ no es lo suficientemente grande respecto a $\sigma$, se debe programar una guarda lógica para truncar la función en cero).*