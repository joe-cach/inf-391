# Unidad 3: Aplicación Práctica y Pruebas de Escritorio (Parte 2)

**Enfoque:** Resolución algorítmica de sistemas complejos mediante variables anidadas y la transición de las pruebas manuales hacia el laboratorio de simulación computacional (Excel y Código).

> **Cita Académica Clave:** > Fishman, G. S. (2001). *Discrete-Event Simulation: Modeling, Programming, and Analysis*. Springer. 
> *(El Capítulo 3 formaliza cómo la composición de múltiples distribuciones simples permite modelar la lógica de sistemas de alta complejidad).*

---

## 3.6.5. Sistemas Complejos: Variables Aleatorias Anidadas

En la Parte 1 resolvimos nodos aislados (un solo rombo o un solo proceso). Sin embargo, en la arquitectura de software real, los diagramas de flujo contienen **condicionales anidados**. Una decisión estocástica a menudo habilita (o bloquea) otra decisión estocástica posterior. 

Para resolver esto en una Prueba de Escritorio, se debe consumir los números generados por el motor $U(0,1)$ de manera estrictamente secuencial, sin reutilizarlos.

### Práctica Integrador: Autenticación y Planes

**El Escenario:**
Modelamos el flujo de *Login* de una plataforma SaaS. 
1. **Filtro 1 (Rombo Booleano):** Cuando una petición llega, tiene un 70% de probabilidad de provenir de un usuario Registrado ($p = 0.70$) y un 30% de ser un Invitado. Si es Invitado, se le rechaza el acceso inmediatamente.
2. **Filtro 2 (Rombo Múltiple):** Si el usuario es Registrado, pasa a un segundo nodo que evalúa su tipo de suscripción histórica: Básico (50%), Pro (30%) o Enterprise (20%).

**Paso 1: Modelado Matemático**
* Filtro 1 (Bernoulli): Éxito si $U \le 0.70$.
* Filtro 2 (Empírica): Básico ($0.00$ a $0.50$), Pro ($0.51$ a $0.80$), Enterprise ($0.81$ a $1.00$).

**Paso 2: Ejecución Manual Secuencial**
Asumimos que nuestro motor computacional ha generado la siguiente secuencia cruda en memoria: $U_1 = 0.85$, $U_2 = 0.45$, $U_3 = 0.62$, $U_4 = 0.12$.

* **Entidad 1 (Llega a la plataforma):**
  * Consume $U_1 = 0.85$ para el Filtro 1. 
  * *Evaluación:* $0.85$ no es menor o igual a $0.70$. Es un Invitado.
  * *Resolución:* **Rechazado.** (La entidad muere aquí. No consume más números).

* **Entidad 2 (Llega a la plataforma):**
  * Consume $U_2 = 0.45$ para el Filtro 1.
  * *Evaluación:* $0.45 \le 0.70$. Es un usuario Registrado.
  * *Tránsito:* Pasa al Filtro 2 y consume el siguiente número en memoria, $U_3 = 0.62$.
  * *Evaluación:* $0.62$ cae en el rango intermedio ($0.51$ a $0.80$).
  * *Resolución:* Usuario Registrado con plan **Pro**.

*Conclusión: Las variables anidadas demuestran cómo el estado de una entidad evoluciona dinámicamente. La Entidad 1 consumió solo un ciclo de reloj (un valor $U$), mientras que la Entidad 2 requirió dos ciclos para completar su viaje por el diagrama.*

---

## 3.6.6. La Transición al Laboratorio: De la Prueba a Excel

Una vez que la arquitectura ha sido validada en papel y la lógica algorítmica es sólida, el siguiente paso de la ingeniería es **escalar**. No podemos simular 10,000 usuarios a mano. Aquí es donde el motor computacional toma el control.

Para visualizar el comportamiento del sistema de forma masiva y estática antes de programarlo en código duro, utilizamos hojas de cálculo como puente. 

**Mapeo de la Matemática a la Hoja de Cálculo:**
1. **La Entidad:** Cada **Fila** del Excel representa una entidad única (un cliente, un paquete de red).
2. **El Motor $U(0,1)$:** Reemplazamos la extracción manual de números por la función nativa `=ALEATORIO()`.
3. **El Moldeado Matemático (Columnas):** Las ecuaciones algebraicas se traducen a fórmulas de celdas.

*Ejemplo de Transición (Distribución Exponencial):*
* Papel (Matemática): $X = -10 \cdot \ln(1 - U)$
* Laboratorio (Excel): `= -10 * LN(1 - ALEATORIO())`

*Ejemplo de Transición (Ruteo de Bernoulli con $p=0.85$):*
* Papel (Lógica): Si $U \le 0.85 \implies \text{Válido}$
* Laboratorio (Excel): `= SI(ALEATORIO() <= 0.85; "Válido"; "Malformado")`

Al arrastrar estas fórmulas hacia abajo por 1,000 filas y presionar la tecla de recálculo (F9), el estudiante podrá observar instantáneamente 1,000 realidades alternativas del comportamiento de su sistema, demostrando el poder del modelado estocástico masivo.

---

## 3.6.7. La Transición a la Memoria RAM: Implementación en Software

El Excel es excelente para el análisis estático y visual, pero carece de la capacidad para manejar **Variables de Estado Concurrentes** (como colas dinámicas, bloqueos de hilos o semáforos en tiempo real). Para construir un simulador real (Arquitectura FEL - *Future Event List*), debemos llevar nuestras variables aleatorias directamente a la memoria RAM usando un lenguaje de programación.

**El Salto Definitivo al Código:**
En código, la inyección matemática se abstrae dentro de funciones utilitarias que el bucle principal de simulación llamará constantemente.

*Ejemplo de implementación pura en Python (Replicando la Transformada Inversa sin usar librerías estadísticas prefabricadas):*

```python
import random
import math

def generar_tiempo_llegada(promedio_beta):
    """
    Inyecta la Transformada Inversa Exponencial
    para modelar cronómetros continuos.
    """
    U = random.random() # Motor U(0,1) crudo
    tiempo = -promedio_beta * math.log(1 - U)
    return tiempo

def evaluar_firewall(probabilidad_exito):
    """
    Inyecta la Distribución de Bernoulli
    para resolver rombos lógicos.
    """
    U = random.random() # Motor U(0,1) crudo
    if U <= probabilidad_exito:
        return "Paquete Válido"
    else:
        return "Paquete Malformado"

# Ejecución del Simulador (Micro-nivel)
print(f"Siguiente petición en: {generar_tiempo_llegada(10):.2f} ms")
print(f"Estado del paquete: {evaluar_firewall(0.85)}")