# Práctica 5: Simulación Avanzada de Service Mesh y Gestión de Secretos en Kubernetes

**Escenario de Estudio:** Clúster K8s, Sidecars (Envoy), Validación mTLS y Extracción de Secretos Criptográficos.
**Objetivo:** Modelar el ciclo de vida de **1000 peticiones RPC (Remote Procedure Call)** internas en un clúster. Se deberá orquestar 8 distribuciones de probabilidad diferentes para predecir cuellos de botella, timeouts y fallos en cadena (Cascading Failures) en la infraestructura de seguridad.

---

## 1. Arquitectura y Flujo del Sistema (Pipeline K8s)

Cuando un Microservicio A solicita un "Secreto" (ej. credenciales de base de datos) al Gestor de Identidad, ocurre lo siguiente:

1. **Llegada (gRPC):** El microservicio emite la petición.
2. **Clasificación del Pod:** El sistema identifica en qué lenguaje corre el Pod solicitante, lo cual afecta el peso del *payload*.
3. **Interceptación Sidecar (Envoy):** El proxy local intercepta el tráfico y añade latencia de enrutamiento.
4. **Validación mTLS:** Se verifica si los certificados de transporte son válidos. Si son inválidos, la conexión hace *Drop* (muere ahí).
5. **Análisis de Grafo de Red:** Un motor de seguridad basado en grafos (Neo4j) evalúa cuántos "saltos" (nodos conexos) existen entre el Pod solicitante y el origen confiable. Cada salto añade fricción.
6. **Resolución IAM:** Se consulta la base de datos principal de roles.
7. **Desencriptación de Secretos:** El Vault abre el anillo criptográfico y extrae el secreto.
8. **Supervivencia (Liveness Probe):** Todo contenedor en K8s tiene un límite de tolerancia. Si la suma total de las latencias (pasos 3 al 7) supera el tiempo de vida (Timeout de hardware), el Kubelet ejecuta un `OOMKilled` o corta la conexión, fracasando la petición.

---

## 2. Modelado Estocástico (8 Variables Aleatorias)

Para cada petición $i$, deberan generar las siguientes variables y aplicar la lógica de ruteo:

**1. Llegadas de Peticiones gRPC (Exponencial)**
*   *Física:* Intervalo entre requests en el clúster. Promedio $\beta = 5$ ms.
*   *Ecuación:* $T_{llegada} = -5 \cdot \ln(1 - U)$

**2. Tipo de Microservicio Solicitante (Empírica)**
*   *Lógica:* K8s aloja distintos lenguajes.
    *   $U \le 0.45 \implies$ "Backend-Go"
    *   $0.45 < U \le 0.80 \implies$ "Worker-Rust"
    *   $U > 0.80 \implies$ "Legacy-NodeJS"

**3. Latencia del Sidecar Envoy (Uniforme Continua)**
*   *Física:* Tiempo que tarda el proxy en parsear las cabeceras gRPC.
*   *Parámetros:* $a = 1$ ms, $b = 4$ ms.

**4. Validación de Certificados mTLS (Bernoulli)**
*   *Lógica:* $U \le 0.985 \implies$ "Válido" (98.5%). Caso contrario $\implies$ "Revocado".
*   *Ruteo:* Si es "Revocado", la transacción muere. Latencias de pasos 5, 6 y 7 se registran como $0$.

**5. Saltos de Auditoría en Grafo (Poisson)**
*   *Física:* Número de nodos en el componente débilmente conexo que el motor de seguridad debe auditar.
*   *Parámetro:* Promedio de saltos $\lambda = 2$.
*   *Impacto:* Cada "salto" detectado añade exactamente **3 ms fijos** a la latencia total.
*   *Nota:* Como Python nativo no tiene Poisson fácil por transformada inversa, deberán usar `numpy.random.poisson(2)`.

**6. Latencia de Base de Datos IAM (Normal)**
*   *Física:* Extracción de políticas RBAC del usuario.
*   *Parámetros:* $\mu = 15$ ms, $\sigma = 4$ ms. *(Usar `random.normalvariate`).*

**7. Tiempo de Desencriptación Criptográfica (Triangular)**
*   *Física:* Tiempo de CPU consumido para abrir el secreto.
*   *Parámetros:* Optimista (Mínimo) = $8$ ms, Probable (Moda) = $12$ ms, Pesimista (Máximo) = $30$ ms.
*   *(Usar `random.triangular(min, max, moda)`).*

**8. Límite de Tolerancia del Kubelet / Timeout (Weibull)**
*   *Física:* El umbral máximo de latencia que el contenedor soporta antes de ser destruido o cancelar el *contexto* de red. Modela hardware que envejece bajo presión.
*   *Parámetros:* Forma $\alpha = 2.5$, Escala $\beta = 50$ ms.
*   *Ecuación:* $T_{limite} = \beta \cdot (-\ln(1 - U))^{(1/\alpha)}$
*   *Lógica Final:* Si la suma de latencias (Envoy + Grafo + IAM + Desencriptación) es mayor a $T_{limite}$, el estado final de la transacción es `"Timeout/Killed"`. De lo contrario, es `"Éxito"`.

---

## 3. Tarea de Laboratorio 

Programe el motor para **1000 peticiones** y consolide los resultados en un DataFrame de `pandas`. Entregue el análisis respondiendo a estas métricas críticas:

1. **Eficiencia del mTLS:** ¿Cuántas peticiones fueron bloqueadas de inmediato por tener un certificado revocado?
2. **Carga Estructural (Grafo):** En promedio, ¿cuánta latencia neta (en ms) añadió el escaneo de nodos conexos al clúster?
3. **Análisis de Resiliencia (Pod Eviction):** De todas las peticiones con mTLS válido, ¿qué porcentaje logró completarse con `"Éxito"` y qué porcentaje terminó en `"Timeout/Killed"` debido al límite de Weibull?
4. **Comportamiento por Lenguaje:** Agrupe por "Tipo de Microservicio". ¿Cuál de los tres lenguajes experimentó la mayor cantidad absoluta de fallos por `"Timeout/Killed"`?
5. **SLA del Sistema:** Para considerar que la infraestructura es de "Grado Empresarial", el percentil 95 ($P_{95}$) de la latencia total de las peticiones exitosas debe ser menor a **45 ms**. Según su simulación, ¿cumplimos con este SLA (Service Level Agreement)?