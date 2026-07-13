# Unidad 1: Introducción a los Modelos y la Simulación
**Bienvenidos.** En esta primera etapa estableceremos el vocabulario técnico universal. Antes de escribir una sola línea de código, necesitamos entender qué estamos observando y cómo aislarlo de la realidad para poder programarlo.

---

## 1.1. El Concepto de Sistema
**¿Qué es?** Un sistema es un conjunto de elementos unidos por relaciones de interacción o interdependencia, que persiguen un fin común. Para estudiarlo, debemos trazar una frontera: todo lo que está dentro es nuestro sistema; lo que está fuera, pero lo afecta, es su entorno.

**Cita Académica:**
> Banks, J., Carson, J. S., Nelson, B. L., & Nicol, D. M. (2010). *Discrete-Event System Simulation*. Prentice Hall.

**Componentes Clave de la Arquitectura de un Sistema:**
* **Entidad:** Cualquier objeto o componente de interés que fluye o existe dentro del sistema (ej. un cliente en un banco, un paquete TCP en una red).
* **Atributo:** Una propiedad o característica que define a una entidad (ej. el saldo de una cuenta, el tamaño en bytes del paquete).
* **Actividad:** Un proceso que provoca cambios y tiene una duración de tiempo física (ej. el servidor atendiendo la petición HTTP).
* **Estado del Sistema:** La "foto" exacta de la memoria. Una colección de variables necesarias para describir todo el sistema en un instante de tiempo $t$ (ej. número de personas en la cola $Q$, estado de la CPU $S$).
* **Evento:** Una ocurrencia instantánea (tiempo $0$) que cambia el estado del sistema (ej. el momento exacto en que termina una descarga).



---

## 1.2. El Concepto de Modelo
**¿Qué es?** Un modelo es una representación simplificada y controlada de un sistema real. Su propósito principal es permitirnos estudiar el comportamiento del sistema sin tener que manipular la infraestructura física, lo cual suele ser costoso, peligroso o directamente imposible.

**Cita Académica:**
> Law, A. M., & Kelton, W. D. (2000). *Simulation Modeling and Analysis*. McGraw-Hill.

**Clasificación Principal:**
* **Modelos Físicos (Icónicos):** Representaciones a escala tangibles. Ejemplos: maquetas en túneles de viento, simuladores de vuelo mecánicos.
* **Modelos Matemáticos / Lógicos:** Representan la lógica del negocio y las relaciones cuantitativas mediante ecuaciones, algoritmos y reglas de estado. *Este es nuestro campo de acción como ingenieros de software.*

---

## 1.3. ¿Qué es la Simulación?
**Definición:** Es el proceso de programar un modelo matemático-lógico de un sistema real en una computadora, y llevar a cabo experimentos con él para comprender su comportamiento a lo largo del tiempo o evaluar nuevas estrategias operativas antes de desplegarlas en producción.

**Cita Académica:**
> Shannon, R. E. (1975). *Systems Simulation: The Art and Science*. Prentice-Hall.

**La Regla de Oro: ¿Cuándo NO se debe simular?**
La simulación es costosa en tiempo y recursos computacionales. No debes usarla si:
1. El problema se puede resolver aplicando el sentido común.
2. Existe una solución analítica matemática exacta y fácil de calcular (ej. un simple sistema de ecuaciones de primer grado).
3. Los costos de desarrollar el simulador superan los ahorros que el proyecto generará.
4. No existen datos históricos, ni estimaciones estadísticas fiables para alimentar el modelo (si entra basura, sale basura).

---

## 1.4. Taxonomía: Clasificación de Modelos (Definiciones Adicionales)
Para construir un simulador, la primera decisión de arquitectura es definir en qué cuadrante de esta taxonomía se encuentra el problema:

**Cita Académica:**
> Zeigler, B. P., Praehofer, H., & Kim, T. G. (2000). *Theory of Modeling and Simulation*. Academic Press.

**A. El Factor del Tiempo:**
* **Estático:** El tiempo no juega ningún rol. Se evalúa un solo instante (ej. Simulación de Montecarlo para calcular el área de una figura compleja o riesgos financieros).
* **Dinámico:** El estado del sistema evoluciona y cambia a lo largo de un eje temporal (ej. la saturación de una red a lo largo del día).

**B. El Factor de Incertidumbre:**
* **Determinístico:** No existen variables aleatorias. Dadas las mismas entradas, el software siempre escupirá exactamente la misma salida. Todo está predefinido.
* **Estocástico:** Contiene al menos una variable generada por azar (ej. el tiempo que tarda un usuario en leer una web). Los resultados de un modelo estocástico no son verdades absolutas, son *estimaciones estadísticas* que requieren miles de corridas.

**C. El Factor de Avance:**
* **Continuo:** El estado cambia de forma ininterrumpida a lo largo del tiempo, gobernado por ecuaciones diferenciales (ej. el nivel de fluidos en una refinería de petróleo, la física de una colisión).
* **Discreto:** La memoria del sistema permanece congelada y solo cambia de forma instantánea mediante "saltos" en puntos de tiempo separados, impulsados exclusivamente por **Eventos**. (ej. el stock de una tienda solo cambia cuando alguien hace clic en "Comprar").