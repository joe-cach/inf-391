# Ejercicio Resuelto 4: Grafo de Eventos Clásico (Sistema de Detección de Fraude con Servidores Paralelos)

## 1. El Escenario del Problema
Un banco cuenta con un sistema que monitorea su red transaccional para detectar operaciones de lavado de dinero. Cuando el algoritmo marca una transacción como "Sospechosa", esta es enviada a un centro de revisión manual.
* El centro cuenta con **dos analistas de seguridad (Servidor A y Servidor B)** trabajando en paralelo.
* Cuando llega una transacción sospechosa, el sistema verifica primero al Analista A. Si está libre, se le asigna.
* Si el Analista A está ocupado, el sistema verifica al Analista B. Si está libre, se le asigna.
* Si ambos están ocupados, la transacción se forma en una única Cola de Espera global.
* Cuando un analista termina, revisa si hay transacciones en la cola. Si hay, toma la primera y comienza a revisarla.

---

## 2. Variables de Estado y Parámetros
Este sistema requiere rastrear el estado de múltiples recursos simultáneamente.

**Variables de Estado:**
* $Q$: Número de transacciones sospechosas en la cola de espera. Inicialmente $Q=0$.
* $S_A$: Estado del Analista A. $S_A=0$ (Libre), $S_A=1$ (Ocupado). Inicialmente $S_A=0$.
* $S_B$: Estado del Analista B. $S_B=0$ (Libre), $S_B=1$ (Ocupado). Inicialmente $S_B=0$.

**Parámetros de Tiempo:**
* $t_a$: Tiempo entre llegadas de transacciones sospechosas.
* $t_{sA}$: Tiempo que tarda el Analista A en revisar (puede ser distinto al de B).
* $t_{sB}$: Tiempo que tarda el Analista B en revisar.

---

## 3. Descripción Formal (La Tupla Matemática)
El Grafo de Eventos se define como $EG=(V, E)$.

### A. Conjunto de Vértices ($V$)
Cada vértice representa un evento y ejecuta la lógica aritmética para actualizar el sistema.

$$V=\{v_0, v_1, v_2, v_3, v_4, v_5\}$$
* $v_0$ (**Inicio**): $Q=0, S_A=0, S_B=0$
* $v_1$ (**Llegada**): $Q=Q+1$ *(La transacción entra directamente a la suma de la cola)*.
* $v_2$ (**Inicio_Revisión_A**): $S_A=1, Q=Q-1$ *(El Analista A toma una transacción de la cola)*.
* $v_3$ (**Fin_Revisión_A**): $S_A=0$ *(El Analista A termina su tarea)*.
* $v_4$ (**Inicio_Revisión_B**): $S_B=1, Q=Q-1$ *(El Analista B toma una transacción de la cola)*.
* $v_5$ (**Fin_Revisión_B**): $S_B=0$ *(El Analista B termina su tarea)*.

### B. Conjunto de Aristas ($E$)
Las condiciones ($c$) aquí son más complejas porque actúan como un balanceador de carga lógico (*Load Balancer*).

**Aristas de Generación:**
* $e_1 = (v_0, v_1, 0, \text{Verdadero})$: Inicia el flujo del motor.
* $e_2 = (v_1, v_1, t_a, \text{Verdadero})$: Bucle infinito de llegada de transacciones sospechosas.

**Aristas de Enrutamiento (Balanceo de Carga en Llegada):**
* $e_3 = (v_1, v_2, 0, [S_A==0])$: Si ocurre una llegada y el Analista A está libre, asignarle el inicio de revisión A de inmediato.
* $e_4 = (v_1, v_4, 0, [S_A==1 \land S_B==0])$: **¡Crucial!** Si ocurre una llegada, A está ocupado, pero B está libre, asignarle el inicio de revisión B. *(Si ambos son 1, no se agenda nada y la transacción se queda acumulada en $Q$)*.

**Aristas del Ciclo de Vida del Analista A:**
* $e_5 = (v_2, v_3, t_{sA}, \text{Verdadero})$: Iniciar en A siempre agenda el Fin de A en un tiempo $t_{sA}$.
* $e_6 = (v_3, v_2, 0, [Q>0])$: Al terminar A, si hay alguien en cola, A vuelve a iniciar servicio.

**Aristas del Ciclo de Vida del Analista B:**
* $e_7 = (v_4, v_5, t_{sB}, \text{Verdadero})$: Iniciar en B siempre agenda el Fin de B en un tiempo $t_{sB}$.
* $e_8 = (v_5, v_4, 0, [Q>0])$: Al terminar B, si hay alguien en cola, B vuelve a iniciar servicio.



---

## 4. Análisis Pedagógico: Orquestación Concurrente
Este ejercicio demuestra la elegancia algorítmica de los Grafos de Eventos de Schruben para manejar paralelismo sin caer en problemas de concurrencia:

1. **La Variable $Q$ como Buffer Universal:** Fíjate que en el evento $v_1$ (Llegada), siempre hacemos $Q = Q + 1$. No importa si el sistema está vacío o lleno. Si el sistema estaba vacío ($S_A=0$), la arista $e_3$ dispara $v_2$ en tiempo 0. El evento $v_2$ inmediatamente ejecuta $Q = Q - 1$. Matemáticamente, la transacción estuvo en la cola durante $0.0$ segundos. Esto simplifica enormemente el código del simulador y evita bugs lógicos.
2. **Prioridad Implícita:** La condición de la arista $e_4$ ($[S_A==1 \land S_B==0]$) establece una prioridad rígida. El Analista B solo recibe trabajo si el Analista A está saturado. Si quisiéramos un balanceo "Round-Robin" (uno y uno), tendríamos que agregar una nueva variable de estado (ej. $Turno \in \{A, B\}$) que altere estas guardas.