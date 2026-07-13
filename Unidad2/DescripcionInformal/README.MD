# Presentación 1: El Modelo Conceptual y la Narrativa Estructurada
**Enfoque:** Abstracción del sistema real y comunicación interdiscursiva.

**Cita Académica:**
> Robinson, S. (2020). *Conceptual Modelling for Simulation: Progress and Grand Challenges*. Journal of Simulation.

**¿Qué es? / Definición o Concepto:**
Antes de escribir una sola línea de código o formular una ecuación, el ingeniero en simulación debe construir un Modelo Conceptual. Esta es la "Descripción Informal", que actúa como puente de comunicación entre el equipo técnico y los expertos del negocio.

**Componentes:**
* **Las Entidades:** Los sujetos u objetos que transitan.
* **El Flujo de Negocio:** El recorrido esperado del sistema.
* **Las Reglas Base:** Las políticas de operación diarias.

**¿Para qué sirve?:**
¿Por qué es informal? Porque los expertos que validarán si tu modelo es correcto no suelen leer código ni diagramas de estado finitos, pero sí entienden narrativas estructuradas y flujos de negocio. Sirve para hablar su mismo idioma.

**Ejemplos:**
* Un gerente de banco verificando las reglas de atención en ventanilla.
* Un médico jefe de urgencias confirmando el protocolo de *triage* (prioridad) de los pacientes.

---

# Presentación 2: Herramientas de Descripción Informal
**Enfoque:** Taxonomía de los artefactos de abstracción.

**Cita Académica:**
> Fishwick, P. A. (1995). *Simulation Model Design and Execution: Building Digital Worlds*. Prentice Hall.

**¿Qué es? / Definición o Concepto:**
Es el conjunto de formatos estandarizados que se utilizan para plasmar el modelo conceptual y transicionar de las ideas habladas a modelos documentados.

**Componentes (Las 3 Herramientas Clave):**
1. **Narrativa Estructurada.**
2. **Diagramas de Bloques (Block Diagrams).**
3. **Diagramas de Flujo Lógico (Flowcharts):**
   * *Subsección Crítica:* Secuencia Lógica (el mapeo de ramificaciones lógicas dentro del flujo).

**¿Para qué sirve?:**
Sirven para tener diferentes "vistas" o "lentes" del sistema (texto, áreas macro y decisiones micro) y documentar formalmente la realidad antes de programar.

**Ejemplos:**
El manual de operaciones de una empresa (Narrativa), el plano de distribución arquitectónica (Bloques) y el manual algorítmico de un sistema informático (Flujo).

---

# Presentación 3: La Narrativa Estructurada
**Enfoque:** Especificación en lenguaje natural restringido.

**Cita Académica:**
> Pidd, M. (2004). *Computer Simulation in Management Science*. Wiley.

**¿Qué es? / Definición o Concepto:**
Un documento escrito en lenguaje natural que detalla de forma determinística las reglas de negocio, los eventos posibles y el flujo de las entidades.

**Componentes:**
* **Sujeto y Acción:** "El cliente llega a la caja".
* **Condicionales de texto:** Uso estricto de palabras como "SI", "ENTONCES", "DE LO CONTRARIO".
* **Eventos del sistema:** Sucesos que cambian la situación (ej. "llega un pedido").

**¿Para qué sirve?:**
Para explicar el funcionamiento del negocio paso a paso, sin usar dibujos ni símbolos, asegurando que todos (tanto programadores como gerentes) entiendan las reglas del juego.

**Ejemplos:**
"SI el cliente tiene tarjeta VIP, ENTONCES avanza a la fila prioritaria. DE LO CONTRARIO, se forma en la fila regular."

---

# Presentación 4: Diagramas de Flujo (Flowcharts)
**Enfoque:** Especificación visual algorítmica.

**Cita Académica:**
> Kelton, W. D., Sadowski, R. P., & Zupick, N. B. (2015). *Simulation With Arena*. McGraw-Hill.

**¿Qué es? / Definición o Concepto:**
El paso intermedio hacia la programación. Son mapas gráficos que utilizan símbolos estandarizados para dictar el recorrido paso a paso de una entidad en el sistema.



**Componentes:**
* **Óvalos/Círculos:** Inicio o fin del proceso.
* **Rectángulos:** Tareas o actividades.
* **Rombos:** Decisiones lógicas.

**¿Para qué sirve?:**
Mapean las decisiones lógicas y los bucles de espera de manera visual para que el programador pueda traducirlo mecánicamente a código fuente (ej. Python, Java).

**Ejemplos:**
Un rombo con la pregunta explícita `¿Servidor libre?`. Si la respuesta es SÍ, una flecha va hacia el rectángulo `Atender`. Si la respuesta es NO, la flecha va hacia un bucle `Esperar`.

---

# Presentación 5: Secuencia Lógica
**Enfoque:** Ramificación exhaustiva de decisiones.

**Cita Académica:**
> Law, A. M. (2015). *Simulation Modeling and Analysis*. McGraw-Hill.

**¿Qué es? / Definición o Concepto:**
Es la disciplina mental que se aplica al construir el diagrama de flujo. Consiste en rastrear absolutamente todos los caminos posibles de una decisión, obligando a que el sistema nunca tenga "puntos muertos".

**Componentes:**
* **La Condición Lógica (Rombo).**
* **La rama clara para Verdad (True).**
* **La rama clara para Falso (False / Estado Alterno).**

**¿Para qué sirve?:**
En la transición a un diagrama de flujo de simulación, el error más común del estudiante de informática es olvidar mapear el "estado alterno". Esta secuencia sirve para garantizar que por cada rombo, existan rutas claras para todas las respuestas.

**Ejemplos:**
Si evaluamos `¿Saldo Suficiente?`, el alumno suele dibujar qué pasa si la respuesta es SÍ (Aprueba la compra), pero se olvida de mapear qué pasa si la respuesta es NO (Rechaza la compra y expulsa a la entidad del sistema).

---

# Presentación 6: Diagramas de Bloques (Block Diagrams)
**Enfoque:** Topología física y conectividad macroscópica.

**Cita Académica:**
> Schriber, T. J. (1974). *Simulation Using GPSS*. John Wiley & Sons.

**¿Qué es? / Definición o Concepto:**
Representaciones visuales de alto nivel que muestran las áreas físicas o lógicas por las que transita una entidad, sin entrar en la lógica condicional fina.



**Componentes:**
* **Bloques Generales:** Representan estaciones de trabajo completas o departamentos.
* **Líneas de conexión direccionales:** Muestran hacia dónde avanza el flujo de trabajo de manera macro.

**¿Para qué sirve?:**
Para observar la estructura del modelo desde arriba ("vista satelital") y comprender las dependencias entre las distintas estaciones del negocio sin distraerse todavía con los rombos de decisión y la secuencia lógica fina.

**Ejemplos:**
Un mapa sencillo con tres rectángulos conectados por flechas: `Recepción` $\to$ `Consultorio` $\to$ `Farmacia`.

---

# Presentación 7: Identificación de Estados de Bloqueo
**Enfoque:** Comportamiento físico ante la saturación de recursos.

**Cita Académica:**
> Banks, J., Carson, J. S., Nelson, B. L., & Nicol, D. M. (2010). *Discrete-Event System Simulation*. Prentice Hall.

**¿Qué es? / Definición o Concepto:**
Es la especificación formal de lo que le ocurre a una entidad cuando avanza por el diagrama de flujo y se topa con un recurso que no está disponible. 

**Componentes:**
En simulación orientada a eventos, es crítico mapear:
* **Entidad Demorada (Delay):** Cuando la entidad entra a un servidor, se programa un evento futuro de salida. (Estado activo consumiendo tiempo).
* **Entidad Encolada (Queue):** Cuando la entidad no encuentra el recurso libre, pasa a un estado pasivo dentro de una lista de espera.

**¿Para qué sirve?:**
Garantiza que el sistema cumpla con las leyes físicas del mundo real (teoría de colas). Las entidades no desaparecen si el servidor está lleno; deben esperar.

**Ejemplos:**
* **Delay:** El tiempo que el mecánico pasa cambiando las llantas de un auto.
* **Queue:** El auto aparcado afuera del taller esperando a que el mecánico termine con el auto anterior.

---

# Presentación 8: Validación del Modelo Conceptual
**Enfoque:** Auditoría y aprobación del diseño.

**Cita Académica:**
> Sargent, R. G. (2013). *Verification and validation of simulation models*. Journal of Simulation.

**¿Qué es? / Definición o Concepto:**
Es el proceso de revisión final. El modelo informal, con su narrativa, flujo y estados de bloqueo ya mapeados, debe someterse a la revisión y aprobación final del "Dueño del Sistema" (el cliente o experto).

**Componentes:**
La auditoría de dos elementos críticos:
1. Las reglas de negocio (¿Falta algo?).
2. Los supuestos del modelo (¿Inventamos algo?).

**¿Para qué sirve?:**
Aquí se busca responder:
* ¿Se han omitido reglas implícitas? 
* ¿Los supuestos son correctos? 

**Ejemplos:**
* Preguntar al experto por reglas ocultas: *"¿Qué pasa si una máquina de lavado se avería en pleno servicio?"*
* Corregir malas suposiciones: *"Asumir que los clientes esperan infinitamente es un supuesto falso en la realidad"*.