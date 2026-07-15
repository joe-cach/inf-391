# Práctica 1: Prueba de Escritorio (Desk Check) Estocástica

**Escenario de Estudio:** Autolavado de Múltiples Servicios (Inyección de Variables Aleatorias).
**Objetivo:** Transicionar del modelo lógico estático (Unidad 2) a un modelo dinámico basado en el tiempo, ejecutando algorítmicamente las ecuaciones matemáticas para procesar 2 vehículos en papel.

---

## 1. Modelado Matemático de Entrada (Input Modeling)

Para darle vida a la narrativa estructurada, el ingeniero de simulación ha extraído los siguientes datos históricos y los ha mapeado a nuestro catálogo de distribuciones:

* **Inyección 1: Evento de Llegada (La Flecha Inicial)**
  * *Comportamiento:* El tiempo entre llegadas de vehículos sigue una distribución **Exponencial**. El promedio histórico es de $\beta = 10$ minutos.
  * *Fórmula generadora:* $T_{llegada} = -10 \ln(1 - U)$

* **Inyección 2: Rombo de Decisión (Tipo de Lavado)**
  * *Comportamiento:* Históricamente, el 40% pide Lavado Rápido y el 60% Lavado Completo. Se usa una distribución **Empírica Discreta**.
  * *Regla Lógica:* * Si $U \le 0.40 \implies$ Lavado Rápido.
    * Si $U > 0.40 \implies$ Lavado Completo.

* **Inyección 3: Rectángulos de Proceso (Demora en Bahía)**
  * *Lavado Rápido:* Tiempo de máquina exacto. Sigue una distribución **Uniforme Continua** entre $5$ y $7$ minutos. 
    * *Fórmula:* $T_{sv} = 5 + U \cdot (7 - 5) = 5 + 2U$
  * *Lavado Completo:* Requiere intervención humana. Sigue una distribución **Uniforme Continua** entre $10$ y $15$ minutos.
    * *Fórmula:* $T_{sv} = 10 + U \cdot (15 - 10) = 10 + 5U$

---

## 2. Inicialización del Motor Estocástico

Para que toda la clase obtenga los mismos resultados en esta prueba manual, el "motor" del sistema ha generado previamente la siguiente cinta de números crudos $U(0,1)$ en la memoria RAM, los cuales deben consumirse estrictamente en orden:

* **Cinta U:** $[U_1 = 0.35, \ U_2 = 0.15, \ U_3 = 0.82, \ U_4 = 0.10, \ U_5 = 0.45, \ U_6 = 0.90]$
* **Reloj del Sistema (T):** $0.00$
* **Estado de Recursos:** Fila = 0/5 | Bahía 1 = Libre | Bahía 2 = Libre

---

## 3. Ejecución Algorítmica Paso a Paso (Traza de Eventos)

### Procesamiento del Vehículo 1
**Paso 1: ¿En qué minuto exacto llega al sistema?**
* Se consume $U_1 = 0.35$.
* Se inyecta a la fórmula de llegadas: 
  $T_{llegada} = -10 \cdot \ln(1 - 0.35) = -10 \cdot \ln(0.65) \approx \mathbf{4.30 \text{ minutos}}$
* **Reloj del Sistema:** Avanza a $T = 4.30$.
* *Condición de fila:* Hay 0 autos. Ingresa y pasa directamente a la **Bahía 1**.

**Paso 2: ¿Qué servicio elige?**
* Se consume $U_2 = 0.15$.
* Se evalúa el rombo lógico: $0.15 \le 0.40$. 
* *Decisión:* Elige **Lavado Rápido**.

**Paso 3: ¿Cuánto tiempo bloqueará la Bahía 1?**
* Se consume $U_3 = 0.82$.
* Se inyecta a la fórmula de Lavado Rápido:
  $T_{sv} = 5 + 2(0.82) = 5 + 1.64 = \mathbf{6.64 \text{ minutos}}$
* *Programación de Salida:* El Vehículo 1 abandonará el sistema en el minuto absoluto $4.30 + 6.64 = \mathbf{10.94}$. (La Bahía 1 queda bloqueada hasta ese momento).

---

### Procesamiento del Vehículo 2
**Paso 4: ¿En qué minuto exacto llega al sistema?**
* Se consume $U_4 = 0.10$.
* Se inyecta a la fórmula de llegadas (calcula el tiempo *desde* el último vehículo):
  $T_{llegada} = -10 \cdot \ln(1 - 0.10) = -10 \cdot \ln(0.90) \approx \mathbf{1.05 \text{ minutos}}$
* **Reloj del Sistema:** Avanza al minuto $4.30 + 1.05 = \mathbf{5.35}$.
* *Evaluación de Recursos:* En el minuto $5.35$, el Vehículo 1 sigue adentro (sale al $10.94$). La Bahía 1 está ocupada. Sin embargo, la **Bahía 2 está libre**. El Vehículo 2 pasa a la Bahía 2 sin hacer fila.

**Paso 5: ¿Qué servicio elige?**
* Se consume $U_5 = 0.45$.
* Se evalúa el rombo lógico: $0.45 > 0.40$.
* *Decisión:* Elige **Lavado Completo**.

**Paso 6: ¿Cuánto tiempo bloqueará la Bahía 2?**
* Se consume $U_6 = 0.90$.
* Se inyecta a la fórmula de Lavado Completo:
  $T_{sv} = 10 + 5(0.90) = 10 + 4.5 = \mathbf{14.50 \text{ minutos}}$
* *Programación de Salida:* El Vehículo 2 abandonará el sistema en el minuto absoluto $5.35 + 14.50 = \mathbf{19.85}$.

---

## 4. Estado Final del Sistema tras la Traza
Al consumir nuestra cinta de 6 números aleatorios, hemos mapeado la siguiente realidad en nuestra arquitectura:
* El **Vehículo 1** entró al $4.30$, tomó servicio Rápido y se fue al $10.94$.
* El **Vehículo 2** entró al $5.35$, tomó servicio Completo y se fue al $19.85$.
* La Fila nunca superó la capacidad de 0, y no se rechazó a ningún cliente.