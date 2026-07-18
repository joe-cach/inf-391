# Práctica 4: Pipeline Estocástico de Procesamiento de Pagos

**Escenario de Estudio:** Microservicio de Pagos, API Antifraude y Gateway Bancario.
**Objetivo:** Modelar el ciclo de vida de una transacción financiera asíncrona, gestionando 6 variables aleatorias (3 continuas y 3 discretas), integrando validaciones en cascada y penalizaciones de latencia de red.

---

## 1. Identificación y Reglas de la Arquitectura

1. **Llegada:** Los *payloads* de cobro llegan al microservicio desde el *frontend* de manera asíncrona.
2. **Clasificación (Bin):** El sistema extrae el BIN de la tarjeta de crédito para identificar la franquicia emisora.
3. **Validación Antifraude (API Externa):** El microservicio envía el *payload* a un proveedor de *Machine Learning* antifraude. Esto genera una latencia de red obligatoria en todos los casos.
4. **Veredicto:** El proveedor responde con un código de estado. Si se etiqueta como fraude, la transacción se bloquea (Drop) y el hilo se libera. Si es válida, avanza.
5. **Autenticación (MFA):** Para transacciones válidas, el sistema evalúa qué nivel de seguridad 3D Secure exige el banco emisor.
6. **Liquidación Bancaria:** La transacción se envía al Gateway del banco para el cobro final, lo cual consume un tiempo de procesamiento pesado antes de devolver el *Status 200 OK*.

---

## 2. Modelado Matemático (Input Modeling)

Se han parametrizado 6 variables aleatorias para este entorno:

*   **Continua 1: Llegadas de Transacciones **
    *   *Física:* Cronómetro entre la llegada de un pago y el siguiente.
    *   *Parámetro:* Promedio de $\beta = 15$ ms.

*   **Discreta 1: Franquicia de la Tarjeta **
    *   *Física:* Distribución del mercado de usuarios.

*   **Continua 2: Latencia de API Antifraude **
    *   *Física:* Demora de ida y vuelta (RTT) del protocolo HTTP hacia el proveedor.
    *   *Parámetros:* $a = 30$ ms, $b = 80$ ms.

*   **Discreta 2: Veredicto de Fraude **
    *   *Física:* Tasa de rechazo por sospecha de tarjeta clonada o sin fondos.

*   **Discreta 3: Requisito MFA **
    *   *Física:* Tipo de validación exigida al usuario final.

*   **Continua 3: Tiempo de Liquidación Bancaria **
    *   *Física:* Demora del sistema *Core* del banco tradicional para confirmar los fondos.
    *   *Parámetros:* Media $\mu = 250$ ms, Desviación Estándar $\sigma = 30$ ms.


---