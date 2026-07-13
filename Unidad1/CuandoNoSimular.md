## ¿Cuándo NO es apropiado simular?

Aunque la simulación es una herramienta de ingeniería extremadamente poderosa, no es la respuesta a todos los problemas. Construir, verificar y validar un modelo de simulación computacional consume una cantidad significativa de tiempo, poder de procesamiento y recursos humanos.

Según la literatura clásica (Banks, Carson, Nelson & Nicol), un ingeniero debe negarse a utilizar la simulación si se cumple alguna de las siguientes condiciones:

1. **Cuando el problema puede resolverse usando el sentido común o lógica simple.**
   > **Ejemplo:** Si el problema es que un servidor de base de datos se queda sin espacio de almacenamiento cada fin de mes porque los logs no se están rotando ni comprimiendo, la solución es implementar una política de *log rotation*, no construir un modelo estocástico de predicción de disco.

2. **Cuando existe una solución analítica exacta.**
   > **Ejemplo:** Si deseas evaluar el peor caso de rendimiento de un algoritmo de ordenamiento sobre un arreglo de datos predecible, no necesitas "simular" su ejecución miles de veces. Utilizas el análisis matemático de Complejidad Algorítmica (Notación Big-O). Si matemáticamente sabes que la complejidad es $O(n^2)$, la solución analítica ya te dio la respuesta exacta.

3. **Cuando es más fácil, barato y rápido realizar experimentos en el sistema real.**
   > **Ejemplo:** Si quieres saber cuánto tiempo tarda en ejecutarse una función *Serverless* (ej. AWS Lambda) con un bloque de código nuevo, es mucho más rápido y barato desplegar la función en un entorno de pruebas (*Staging*) y medir los tiempos de ejecución reales (*Load Testing* con herramientas como JMeter), que intentar construir un modelo matemático que simule la arquitectura interna de los servidores de Amazon.

4. **Cuando los costos de la simulación superan los beneficios esperados.**
   > **Ejemplo:** Un equipo de desarrollo necesita optimizar la interfaz gráfica de una aplicación web interna usada por 5 empleados. Construir un modelo de simulación del comportamiento de los usuarios (tiempos de clic, navegación estocástica) tomaría 3 semanas. Modificar el código y hacer pruebas A/B reales tomaría 2 días. El costo de simular es injustificable.

5. **Cuando no hay datos disponibles o los datos son de mala calidad.**
   > **Ejemplo:** Te piden simular la concurrencia y los cuellos de botella de una red *blockchain* revolucionaria que aún no existe y para la cual no existen registros históricos de comportamiento de usuarios (Logs, Trazas de red, Métricas). Sin datos de entrada válidos, las variables aleatorias se basarán en conjeturas puras. Como dicta el principio de sistemas: GIGO (*Garbage In, Garbage Out*).

6. **Cuando el sistema es demasiado complejo para ser definido lógicamente.**
   > **Ejemplo:** Intentar simular computacionalmente la ingeniería social en ciberseguridad. El comportamiento y la psicología de un usuario humano que decide hacer clic en un correo de *Phishing* obedece a factores emocionales y cognitivos que no pueden modelarse fielmente mediante ecuaciones matemáticas o distribuciones probabilísticas cerradas.

7. **Cuando las expectativas del tomador de decisiones son irracionales.**
   > **Ejemplo:** Si la gerencia te pide "simular el sistema para que nos devuelva la arquitectura óptima". La simulación estocástica *no optimiza*. Un simulador no genera soluciones por sí mismo; solo evalúa escenarios (entradas) que el ingeniero propone y devuelve resultados estadísticos (salidas). Si buscan optimización automática para un problema determinístico, deben usar Investigación de Operaciones (Programación Lineal/Dinámica), no simulación.