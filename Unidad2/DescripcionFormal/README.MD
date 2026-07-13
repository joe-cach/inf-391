# Presentación 1: Máquinas de Estados Finitos (FSM) y sus Variaciones
**Enfoque:** Lógica secuencial, control de estados y sistemas determinísticos.

---

## 1. FSM Clásica (Finite State Machine)
**¿Qué es?** El modelo matemático base para representar sistemas mediante estados lógicos discretos que cambian instantáneamente al recibir un estímulo (evento) válido. No tiene noción del tiempo físico ni memoria acumulativa.

**Cita Académica:**
> Cassandras, C. G., & Lafortune, S. (2008). *Introduction to Discrete Event Systems*. Springer.

**Definición Matemática Estricta:**
$$G = (S, E, f, \Gamma, s_0)$$

**Componentes:**
* **$S$**: Conjunto finito de estados lógicos.
* **$E$**: Conjunto finito de eventos (estímulos).
* **$f$**: Función de transición de estados ($f: S \times E \to S$). Es el motor que actualiza el estado.
* **$\Gamma$**: Función de factibilidad ($\Gamma: S \to 2^E$). El "guardia" que define qué eventos están permitidos en el estado actual.
* **$s_0$**: Estado inicial. Condición obligatoria de arranque en $t=0$.

**¿Para qué sirve?**
Modelado de ciclos de vida estrictos y algoritmos de control básicos (ej. el ciclo de vida de un proceso en el SO: Nuevo -> Listo -> Ejecución).

---

## 2. EFSM (Extended Finite State Machine)
**¿Qué es?** Una FSM a la que se le inyecta un bloque de memoria (Variables de Contexto). Transforma los eventos en "eventos parametrizados" e introduce **Guardas Lógicas** para evitar la explosión geométrica de estados.

**Cita Académica:**
> Cheng, K. T., & Krishnakumar, A. S. (1993). *Automatic Generation of Functional Vectors Using the Extended Finite State Machine Model*. IEEE.

**Definición Matemática Estricta:**
$$G_E = (S, E, V, \Gamma, f, s_0, v_0)$$

**Componentes Nuevos:**
* **$V$**: Conjunto de variables de memoria (ej. contadores, saldos numéricos).
* **$v_0$**: Vector inicial de las variables de memoria al encender el sistema.
* **$\Gamma$**: Ahora evalúa Guardas Lógicas ($\Gamma: S \times V \to 2^E$).
* **$f$**: Ahora ejecuta Acciones sobre la memoria ($f: S \times E \times V \to S \times V$).

**¿Para qué sirve?**
Modelado de interfaces de usuario complejas, cajeros automáticos, máquinas expendedoras y protocolos de red TCP/IP donde se debe rastrear información cuantitativa.

---

## 3. Statecharts (Grafos de Estado de Harel)
**¿Qué es?** La evolución visual y matemática de la FSM orientada a sistemas complejos. Introduce dos superpoderes: **Jerarquía** (estados anidados) y **Ortogonalidad** (concurrencia paralela).

**Cita Académica:**
> Harel, D. (1987). *Statecharts: A visual formalism for complex systems*. Science of Computer Programming.

**Definición Matemática Básica:**
$$ST = (S, E, \delta, H, s_0)$$

**Componentes Clave:**
* **$H$**: Función de jerarquía ($\rho: S \to 2^S$). Permite agrupar estados dentro de "Súper-estados".
* **$\delta$**: Función de transición que soporta ejecución paralela de múltiples autómatas simultáneamente.

**¿Para qué sirve?**
Es el estándar de la industria (UML) para la arquitectura de software orientado a objetos. Ejemplo: El software de un automóvil, donde la radio y los limpiaparabrisas operan en paralelo dentro del estado "Vehículo Encendido".

---

## 4. Autómatas Temporizados (Timed Automata)
**¿Qué es?** Una FSM acoplada a variables de "relojes continuos". Las transiciones de estado están estrictamente obligadas a ocurrir dentro de ventanas de tiempo exactas.

**Cita Académica:**
> Alur, R., & Dill, D. L. (1994). *A theory of timed automata*. Theoretical Computer Science.

**Definición Matemática Estricta:**
$$TA = (L, l_0, \Sigma, X, I, E)$$

**Componentes Clave:**
* **$L$**: Localidades (Nodos).
* **$X$**: Conjunto de relojes continuos reales ($x \in \mathbb{R}^+$).
* **$I$**: Invariantes de tiempo (Límites máximos que un sistema puede permanecer en una localidad).
* **$E$**: Aristas que contienen guardas de tiempo y reseteo de relojes.

**¿Para qué sirve?**
Ingeniería de Sistemas de Tiempo Real (Real-Time Systems). Ejemplo: El software de despliegue de un Airbag o los frenos ABS.

---
---

# Presentación 2: Redes de Petri y sus Variaciones
**Enfoque:** Paralelismo, sincronización, competencia por recursos compartidos y cuellos de botella.

---

## 1. Redes de Petri Clásicas (Place/Transition Nets)
**¿Qué es?** Un formalismo basado en grafos bipartitos para describir sistemas distribuidos. Utiliza "Tokens" anónimos para representar la disponibilidad de un recurso.

**Cita Académica:**
> Peterson, J. L. (1981). *Petri Net Theory and the Modeling of Systems*. Prentice Hall.

**Definición Matemática Estricta:**
$$PN = (P, T, F, W, M_0)$$

**Componentes:**
* **$P$**: Conjunto de Lugares (Círculos, representan condiciones o recursos).
* **$T$**: Conjunto de Transiciones (Rectángulos, representan eventos).
* **$F$**: Relación de Flujo (Arcos direccionales que conectan $P \to T$ o $T \to P$).
* **$W$**: Función de Peso ($W: F \to \mathbb{N}^+$). Define cuántos tokens se consumen/producen.
* **$M_0$**: Vector de Marcado Inicial ($M_0: P \to \mathbb{N}$). La distribución de tokens en $t=0$.

**¿Para qué sirve?**
Análisis de exclusión mutua (Mutex), prevención de Deadlocks (bloqueos) e inanición en hilos de procesamiento de CPU concurrentes.

---

## 2. Redes de Petri Coloreadas (CPN)
**¿Qué es?** Extiende las Redes Clásicas dándole "Color" a los tokens. Los tokens ya no son puntos ciegos, sino objetos de datos complejos (variables, structs, JSON).

**Cita Académica:**
> Jensen, K. (1992). *Coloured Petri Nets. Basic Concepts, Analysis Methods and Practical Use*. Springer.

**Definición Matemática Estricta:**
$$CPN = (\Sigma, P, T, A, N, C, G, E, I)$$

**Componentes Clave:**
* **$\Sigma$**: Conjunto finito de tipos de datos (Los "Colores").
* **$C$**: Función que tipa los Lugares (ej. Este lugar solo acepta tokens de tipo "Paquete TCP").
* **$G$**: Función de Guarda en las Transiciones (Condicionales para el flujo de datos).
* **$E$**: Expresiones funcionales en los arcos para modificar los datos del token en tránsito.

**¿Para qué sirve?**
Modelado de bases de datos transaccionales, enrutamiento avanzado en telecomunicaciones y validación de protocolos de red.

---

## 3. Redes de Petri Estocásticas (SPN y GSPN)
**¿Qué es?** Inyectan variables aleatorias al tiempo que tarda una Transición en dispararse. Permiten evaluar el rendimiento bajo incertidumbre, vinculando las Redes de Petri con las Cadenas de Markov.

**Cita Académica:**
> Molloy, M. K. (1982). *Performance Analysis Using Stochastic Petri Nets*. / Ajmone Marsan et al. (1984). *GSPN*.

**Definición Matemática Estricta (SPN):**
$$SPN = (P, T, F, W, M_0, \Lambda)$$

**Componentes Clave:**
* **$\Lambda$**: Función ($\Lambda: T \to \mathbb{R}^+$) que asocia a cada transición una tasa de disparo exponencial aleatoria ($\lambda$).
* **GSPN (Generalizadas):** Divide las transiciones en *Temporizadas* (tardan tiempo aleatorio) e *Inmediatas* (tiempo cero, decisiones lógicas).

**¿Para qué sirve?**
Análisis de rendimiento, cálculo de tiempos de espera en servidores y dimensionamiento de infraestructura (Capacity Planning).

---
---

# Presentación 3: Grafos de Eventos (Event Graphs)
**Enfoque:** Algoritmia del motor de simulación y gestión de la Lista de Eventos Futuros (FEL).

---

## 1. Grafos de Eventos Clásicos (Schruben)
**¿Qué es?** El puente definitivo entre el modelo matemático y el código fuente. Modela gráficamente cómo la ocurrencia de un evento en el presente "agenda" la ocurrencia de otro evento en el futuro.

**Cita Académica:**
> Schruben, L. (1983). *Simulation Modeling with Event Graphs*. Communications of the ACM.

**Definición Matemática Estricta:**
$$EG = (V, E)$$

**Componentes:**
* **$V$**: Conjunto de Vértices (Eventos que alteran el estado del sistema, ej. *Llegada*).
* **$E$**: Conjunto de Aristas Direccionales entre vértices, definidas por $(t, c)$.
    * **$t$**: Retraso temporal para agendar el próximo evento (frecuentemente estocástico).
    * **$c$**: Condición o guarda lógica que debe cumplirse para poder agendar el evento.

**¿Para qué sirve?**
Es el plano arquitectónico directo para programar el bucle principal (`while`) de un motor de simulación de eventos discretos. Define cómo se alimenta la Future Event List (FEL).

---

## 2. Grafos de Eventos Parametrizados (PEG)
**¿Qué es?** La versión orientada a objetos del Grafo de Eventos. Permite que los eventos transfieran información contextual (argumentos) a los eventos futuros que están agendando en la FEL.

**Cita Académica:**
> Som, T. K., & Sargent, R. G. (1989). *A formal development of event graphs as an algorithm specification language*.

**Componentes Clave:**
* Cada vértice $v(k)$ acepta un vector de parámetros.
* Cada arista pasa funciones de atributos $p$. (Ej. El evento *Llegada(Cliente_5)* agenda el evento *Inicio_Servicio(Cliente_5)*).

**¿Para qué sirve?**
Indispensable para programar simuladores modernos y recolectar estadísticas individualizadas (rastrear a una entidad específica desde que entra hasta que sale del sistema).