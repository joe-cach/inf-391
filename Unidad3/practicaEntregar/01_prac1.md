## 8. Ejercicio Combinado: E-commerce "OmniMarket Suite"

**Escenario:** El *Load Balancer* de una plataforma de comercio electrónico ficticia llamada **OmniMarket** procesa el tráfico de miles de usuarios concurrentes. Por cada sesión que ingresa al sistema, simularemos tres comportamientos independientes que dictan la carga de la infraestructura:

1.  **¿Qué acción realiza el usuario? (Distribución Empírica Discreta)**
    El departamento de analítica indica que el comportamiento de los usuarios se divide en:
    * Navegación de Catálogo: $55\%$
    * Añadir al Carrito: $30\%$
    * Checkout / Pago: $15\%$
2.  **¿A qué clúster se enruta la sesión? (Distribución Uniforme Discreta)**
    La arquitectura opera con **5 clústeres** regionales (numerados del 1 al 5) operando bajo un balanceo de carga estricto tipo *Round-Robin*, donde todos tienen la misma probabilidad de recibir la sesión.
3.  **¿Cuántas consultas a la base de datos genera? (Distribución de Poisson)**
    Dependiendo del volumen del catálogo, la cantidad de peticiones al motor de base de datos "QuantumDB" sigue un comportamiento de Poisson con un promedio de $\lambda = 12$ consultas (*queries*) por sesión.

---

