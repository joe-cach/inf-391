# Práctica 2: Prueba de Escritorio (Desk Check) - Redes y Cuellos de Botella

**Escenario de Estudio:** Enrutador con Buffer Limitado (Packet Drop).
**Objetivo:** Ejecutar la traza de eventos de un sistema donde la saturación de recursos provoca el descarte físico de entidades, controlando el reloj del sistema (Time-Advance) mediante variables continuas.

---

## 1. Identificación y Reglas de la Arquitectura
* **Entidades:** Paquetes de Red.
* **Recursos:** 1 Canal de Procesamiento (CPU) y 1 Buffer de Memoria (Cola).
* **Restricción Crítica:** El Buffer tiene una capacidad estricta de `MAX = 2`. 
* **Regla de Negocio:** Si un paquete llega en el instante temporal $T$, y en ese exacto milisegundo la CPU está ocupada AND el Buffer tiene 2 paquetes esperando, el paquete entrante se descarta irrevocablemente (*Drop*).

---

## 2. Modelado Matemático de Entrada (Input Modeling)

Para esta arquitectura, el ingeniero de simulación ha parametrizado el sistema operando en milisegundos (ms):

* **Inyección 1: Evento de Llegada (Inter-Arrival Time)**
  * *Comportamiento:* Las peticiones de red llegan de manera asíncrona. Siguen una distribución **Exponencial** con un tiempo promedio de $\beta = 5$ ms.
  * *Fórmula generadora:* $T_{llegada} = -5 \ln(1 - U)$

* **Inyección 2: Rectángulo de Proceso (Tiempo de CPU)**
  * *Comportamiento:* El procesamiento criptográfico de la CPU varía muy poco. Sigue una distribución **Uniforme Continua** entre $a = 2$ y $b = 4$ ms.
  * *Fórmula generadora:* $T_{cpu} = 2 + U \cdot (4 - 2) = 2 + 2U$

---

## 3. Inicialización del Motor Estocástico

Para garantizar que todos los ingenieros obtengan el mismo comportamiento de saturación durante la auditoría manual, el motor ha reservado la siguiente secuencia de números crudos en memoria:

* **Cinta U:** $[U_1 = 0.30, \ U_2 = 0.85, \ U_3 = 0.25, \ U_4 = 0.20, \ U_5 = 0.15, \ U_6 = 0.60]$
* **Reloj del Sistema (T):** $0.00$ ms
* **Estado de Recursos inicial:** CPU = Libre | Buffer = 0/2

---

## 4. Ejecución Algorítmica Paso a Paso

### Procesamiento del Paquete 1 (P1)
**Paso 1: Llegada al Sistema**
* Se consume $U_1 = 0.30$.
* $T_{llegada} = -5 \cdot \ln(1 - 0.30) = -5 \cdot \ln(0.70) \approx \mathbf{1.78 \text{ ms}}$.
* **Reloj (T):** $1.78$ ms.
* *Estado:* CPU libre. P1 entra directamente al procesador.

**Paso 2: Procesamiento en CPU**
* Se consume $U_2 = 0.85$.
* $T_{cpu} = 2 + 2(0.85) = 2 + 1.70 = \mathbf{3.70 \text{ ms}}$.
* *Programación:* La CPU estará bloqueada por P1 hasta el milisegundo absoluto $1.78 + 3.70 = \mathbf{5.48 \text{ ms}}$.

---

### Procesamiento del Paquete 2 (P2)
**Paso 3: Llegada al Sistema**
* Se consume $U_3 = 0.25$.
* $T_{llegada} = -5 \cdot \ln(1 - 0.25) = -5 \cdot \ln(0.75) \approx \mathbf{1.43 \text{ ms}}$.
* **Reloj (T):** $1.78 + 1.43 = \mathbf{3.21 \text{ ms}}$.
* *Evaluación:* En el ms $3.21$, la CPU sigue bloqueada por P1 (hasta el $5.48$).
* *Estado:* P2 entra al Buffer. **(Buffer: 1/2)**.

---

### Procesamiento del Paquete 3 (P3)
**Paso 4: Llegada al Sistema**
* Se consume $U_4 = 0.20$.
* $T_{llegada} = -5 \cdot \ln(1 - 0.20) = -5 \cdot \ln(0.80) \approx \mathbf{1.11 \text{ ms}}$.
* **Reloj (T):** $3.21 + 1.11 = \mathbf{4.32 \text{ ms}}$.
* *Evaluación:* En el ms $4.32$, la CPU sigue bloqueada por P1.
* *Estado:* P3 entra al Buffer. **(Buffer: 2/2)** $\rightarrow$ *¡ALERTA: BUFFER LLENO!*

---

### Procesamiento del Paquete 4 (P4)
**Paso 5: Llegada al Sistema**
* Se consume $U_5 = 0.15$.
* $T_{llegada} = -5 \cdot \ln(1 - 0.15) = -5 \cdot \ln(0.85) \approx \mathbf{0.81 \text{ ms}}$.
* **Reloj (T):** $4.32 + 0.81 = \mathbf{5.13 \text{ ms}}$.
* *Evaluación:* En el ms $5.13$, la CPU sigue bloqueada por P1 (se libera en el $5.48$). El Buffer está al 100% de su capacidad (2/2).
* *Estado:* **¡PACKET DROP!** El Paquete 4 es destruido por el enrutador. No consume tiempo de procesamiento.

---

### Liberación y Avance de Cola
**Paso 6: P1 termina y P2 entra a CPU**
* El reloj avanza al ms **$5.48$**. P1 sale del sistema.
* La CPU queda libre. Inmediatamente extrae a P2 del Buffer. **(Buffer baja a: 1/2)**.
* Se consume $U_6 = 0.60$ para calcular el procesamiento de P2.
* $T_{cpu} = 2 + 2(0.60) = 2 + 1.20 = \mathbf{3.20 \text{ ms}}$.
* *Programación:* P2 bloqueará la CPU desde el ms $5.48$ hasta el $5.48 + 3.20 = \mathbf{8.68 \text{ ms}}$.

---

## 5. Conclusiones de la Prueba
A través de la matemática, hemos comprobado un fallo arquitectónico: el sistema es demasiado lento. La CPU promedia tiempos de proceso altos (ej. 3.70 ms), mientras que la red inyecta paquetes muy rápido (1.43, 1.11, 0.81 ms). 

El alumno puede observar que sin escribir una sola línea de código, la simulación manual nos permitió auditar la pérdida de datos y justificar la necesidad técnica de aumentar el tamaño de la memoria RAM del Buffer o escalar verticalmente a una CPU más rápida.