## 9. Ejercicio Combinado: Pipeline CI/CD "OmniMarket" (Variables Continuas)

**Escenario:** El equipo de Ingeniería de Software de **OmniMarket** necesita simular la latencia y los tiempos operativos de su *Pipeline* de Despliegue Continuo (CI/CD). Como estamos midiendo el "tiempo" (que puede tener infinitos decimales), utilizaremos **tres distribuciones continuas** encadenadas para simular el ciclo de vida de 1,000 *commits* de código:

1.  **Tiempo entre Commits (Distribución Exponencial):** Los desarrolladores empujan código de forma asíncrona a lo largo del día. Típicamente, llega un nuevo *commit* cada $\beta = 15$ minutos.
2.  **Tiempo de Compilación / Build (Distribución Triangular):** El servidor CI compila el monolito de OmniMarket. Los ingenieros estiman que tarda un mínimo de $a = 3$ min, un tiempo más probable de $c = 5$ min, y un máximo de $b = 12$ min si hay conflictos de dependencias.
3.  **Tiempo de Despliegue en Red (Distribución Lognormal):** Empujar la imagen del contenedor a los nodos de producción suele ser rápido, pero las congestiones de red crean una asimetría extrema (Cola Larga). Usaremos $\mu = 1.2$ y $\sigma = 0.6$ (escala logarítmica).

---

