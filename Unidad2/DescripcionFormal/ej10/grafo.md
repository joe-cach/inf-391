# Ejercicio Resuelto 3: Grafo de Eventos Clásico (Cola de un solo Servidor)

## 1. El Escenario del Problema
Se desea simular el comportamiento de un **Servidor Web de un solo hilo (Single-Thread)**. 
* Las peticiones (usuarios) llegan al servidor de forma aleatoria.
* Si la CPU está libre, la petición se atiende de inmediato.
* Si la CPU está ocupada, la petición se forma en una cola de espera (Buffer).
* Al terminar de procesar una petición, si hay peticiones esperando en la cola, la CPU toma la primera de la fila y la procesa. Si no hay nadie, la CPU se queda inactiva (Libre).

---

## 2. Variables de Estado y Parámetros
Antes de dibujar el grafo, debemos definir la memoria del sistema (Variables) y los tiempos (Parámetros).

**Variables de Estado (Cambian durante la simulación):**
* $Q$: Longitud de la cola (Número de peticiones esperando). Inicialmente $Q=0$.
* $S$: Estado de la CPU. $S=0$ (Libre), $S=1$ (Ocupada). Inicialmente $S=0$.

**Parámetros de Tiempo (Generadores Aleatorios):**
* $t_a$: Tiempo entre llegadas de peticiones.
* $t_s$: Tiempo de servicio (lo que tarda la CPU en procesar la petición).

---

## 3. Descripción Formal (La Tupla Matemática)
El Grafo de Eventos se define matemáticamente como un grafo dirigido: 
$$EG=(V, E)$$

### A. Conjunto de Vértices ($V$)
Los vértices representan los **Eventos**. Un evento es un punto en el tiempo donde ocurre un cambio de estado. Cada vértice contiene la lógica de actualización (la función matemática $f$).

$$V=\{v_0, v_1, v_2, v_3\}$$
* $v_0$ (**Inicio**): Arranca la simulación.
  * *Acción:* $Q=0, S=0$
* $v_1$ (**Llegada**): Un usuario entra al sistema.
  * *Acción:* $Q=Q+1$
* $v_2$ (**Inicio_Servicio**): La CPU toma a un usuario.
  * *Acción:* $S=1, Q=Q-1$
* $v_3$ (**Fin_Servicio**): La CPU termina de procesar.
  * *Acción:* $S=0$

### B. Conjunto de Aristas ($E$)
Las aristas (flechas) representan la **Planificación de Eventos**. Responden a la pregunta: *"Si ocurre este evento, ¿qué otro evento se debe programar en el futuro?"*
Cada arista se define como una tupla: $(Origen, Destino, Retraso\_Tiempo, Condición)$.

* $e_1 = (v_0, v_1, 0, \text{Verdadero})$: El Inicio agenda la primera Llegada en el tiempo 0.
* $e_2 = (v_1, v_1, t_a, \text{Verdadero})$: **Bucle de Generación.** Cada vez que ocurre una Llegada, se agenda automáticamente la *siguiente* Llegada en un tiempo aleatorio $t_a$.
* $e_3 = (v_1, v_2, 0, [S==0])$: Si ocurre una Llegada y la CPU está libre ($S==0$), se agenda un Inicio_Servicio inmediatamente (tiempo 0).
* $e_4 = (v_2, v_3, t_s, \text{Verdadero})$: Cuando inicia un servicio, se agenda obligatoriamente el Fin_Servicio en un tiempo $t_s$.
* $e_5 = (v_3, v_2, 0, [Q>0])$: Cuando termina un servicio, **SI** hay alguien en la cola ($Q>0$), se agenda de inmediato un nuevo Inicio_Servicio.



---

## 4. Análisis Pedagógico: ¿Cómo se lee este Grafo?
El Grafo de Eventos de Schruben es el "código fuente" visual de un simulador estocástico. Se lee como un motor de causa y efecto mediado por el tiempo.

1. **La Condición Inicial:** El evento $v_0$ arranca el motor. Sin él, la Lista de Eventos Futuros (FEL) estaría vacía y el simulador moriría.
2. **El Bucle Infinito de Clientes:** La arista recursiva $(v_1 \to v_1)$ con retraso $t_a$ es el secreto de la simulación. Asegura que mientras el programa corra, siempre habrá un flujo constante de entidades llegando, sin necesidad de un bucle `while` para crearlas.
3. **Las Guardas Condicionales (Corchetes):** * La arista $v_1 \to v_2$ solo permite cruzar si $S==0$. Si la CPU está ocupada, la arista se ignora, el evento de servicio no se agenda, y el cliente simplemente se queda "atrapado" sumado en la variable $Q$ (en la cola).
   * La arista $v_3 \to v_2$ rescata a esos clientes. Al terminar de atender, la CPU verifica si $Q>0$. Si es cierto, extrae al cliente atrapado y lo procesa.

**Traducción a Código:** En el Tema 4 de la materia, cada vértice de este grafo se programará como una función (`def llegada():`, `def fin_servicio():`) y cada arista será una instrucción de inserción en la Lista de Eventos Futuros (`FEL.insertar(tiempo_actual + t_a, "Llegada")`).