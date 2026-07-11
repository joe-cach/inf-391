# Ejercicio Resuelto 2: Red de Petri Coloreada (CPN) - Servidor de Autenticación API

## 1. El Escenario del Problema
Un backend de Microservicios procesa solicitudes de usuarios. Para atender una petición, el sistema requiere validar un token de acceso (JWT). 
* El sistema maneja dos categorías de usuarios: `Premium` (máxima prioridad, procesamiento inmediato) y `Regular` (procesamiento estándar).
* El Servidor de Autenticación extrae las peticiones de un buffer de entrada, evalúa el tipo de usuario mediante una **Guarda Lógica** y despacha la petición a la cola de ejecución correspondiente.

---

## 2. Descripción Formal (La Tupla Matemática)
Toda Red de Petri Coloreada se define estrictamente mediante la tupla: 
$$CPN=(\Sigma, P, T, A, N, C, G, E, I)$$

A continuación, adaptamos cada componente para resolver nuestro problema informático:

### A. Conjunto de Tipos de Datos o Colores ($\Sigma$)
Definimos el "Color" de los tokens. Los tokens ya no son puntos negros anónimos, ahora son estructuras de datos (*structs*).
$$\Sigma=\{\text{TipoUsuario}, \text{Peticion}\}$$
* `TipoUsuario` = Enumerable con valores `{PREMIUM, REGULAR}`.
* `Peticion` = Registro o Struct definido como: `{id: Int, tipo: TipoUsuario}`.

### B. Conjunto de Lugares ($P$) y Función de Tipo ($C$)
Los lugares (círculos) almacenan colecciones de tokens de un color específico determinado por la función $C: P \to \Sigma$.
$$P=\{p_1, p_2, p_3\}$$
* $p_1$: **Buffer de Entrada**. Tipo de Color: `Peticion`. *(Almacena los paquetes crudos que llegan de la red).*
* $p_2$: **Fila de Ejecución Premium**. Tipo de Color: `Peticion`. *(Solo admite usuarios Premium).*
* $p_3$: **Fila de Ejecución Regular**. Tipo de Color: `Peticion`. *(Solo admite usuarios Regulares).*

### C. Conjunto de Transiciones ($T$) y Sus Guardas ($G$)
Las transiciones (rectángulos) ejecutan el filtrado e introducen **Guardas Lógicas** $G(t)$ que evalúan las propiedades internas del token.
$$T=\{t_1, t_2\}$$
* $t_1$: **Clasificar Petición Premium**. 
  * Guarda: $G(t_1)=[\text{req.tipo}==\text{PREMIUM}]$
* $t_2$: **Clasificar Petición Regular**. 
  * Guarda: $G(t_2)=[\text{req.tipo}==\text{REGULAR}]$

### D. Arcos ($A$), Nodos ($N$) y Expresiones de Arco ($E$)
Las expresiones de arco $E$ actúan como variables que capturan el token en tránsito. Definimos la variable `req` de tipo `Peticion`.

**Para la Transición $t_1$ (Ruta Premium):**
* Arco entrada $p_1 \to t_1$: Expresión = `req` *(Extrae una petición del buffer).*
* Arco salida $t_1 \to p_2$: Expresión = `req` *(Deposita la misma petición en la fila VIP).*

**Para la Transición $t_2$ (Ruta Estándar):**
* Arco entrada $p_1 \to t_2$: Expresión = `req`
* Arco salida $t_2 \to p_3$: Expresión = `req`

### E. Marcado Inicial ($M_0$)
En el instante $t=0$, el Buffer de Entrada ($p_1$) ha recibido tres peticiones de la red, mientras que las colas de procesamiento están vacías. El marcado se expresa como un conjunto múltiple (*Multiset*):

* $M_0(p_1)=1 \cdot \{\text{id}: 101, \text{tipo}: \text{REGULAR}\} + 1 \cdot \{\text{id}: 102, \text{tipo}: \text{PREMIUM}\} + 1 \cdot \{\text{id}: 103, \text{tipo}: \text{REGULAR}\}$
* $M_0(p_2)=\emptyset$ *(Vacío)*
* $M_0(p_3)=\emptyset$ *(Vacío)*

---

## 3. Resolución Analítica (Análisis de Habilitación y Disparo)

A diferencia de las redes clásicas donde solo contamos enteros, en papel analizamos la habilitación mediante la asignación de variables (*Binding*). Evaluamos el token de la petición `102`: `req = {id: 102, tipo: PREMIUM}`.

### Paso 1: Evaluación de Habilitación ($\Gamma$)
* **Para $t_2$:** Se evalúa la guarda $G(t_2)=[\text{req.tipo}==\text{REGULAR}] \implies [\text{PREMIUM}==\text{REGULAR}] \equiv \text{FALSO}$. 
  * *Resultado:* $t_2$ **NO** está habilitada para este token.
* **Para $t_1$:** Se evalúa la guarda $G(t_1)=[\text{req.tipo}==\text{PREMIUM}] \implies [\text{PREMIUM}==\text{PREMIUM}] \equiv \text{VERDADERO}$.
  * *Resultado:* $t_1$ **SÍ** está habilitada. El "guardia" del microservicio permite el cruce.



---

## 4. Nuevo Marcado del Sistema ($M_1$)
Al ejecutarse el disparo de la transición $t_1$ con el *binding* de la petición `102`, el token es removido del buffer de entrada y transferido al buffer exclusivo de alta prioridad.

El nuevo estado matemático de la base de datos distribuida es:
* $M_1(p_1)=1 \cdot \{\text{id}: 101, \text{tipo}: \text{REGULAR}\} + 1 \cdot \{\text{id}: 103, \text{tipo}: \text{REGULAR}\}$ *(El token 102 ya no está aquí).*
* $M_1(p_2)=1 \cdot \{\text{id}: 102, \text{tipo}: \text{PREMIUM}\}$ *(El token VIP ingresó con éxito a su zona de ejecución).*
* $M_1(p_3)=\emptyset$

**Conclusión Pedagógica:** La Red de Petri Coloreada demuestra cómo un único lugar de almacenamiento ($p_1$) puede gestionar múltiples tipos de datos concurrentes y cómo las transiciones, actuando como enrutadores lógicos de software, segmentan la carga de trabajo de manera determinística sin sufrir explosión de estados.