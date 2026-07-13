# Práctica 2: Clasificación Taxonómica

Analiza cuidadosamente los siguientes 10 sistemas. Clasifícalos según la taxonomía aprendida marcando la categoría correspondiente y justifica tu respuesta en una oración breve.

## Sistemas a clasificar:
1. El decaimiento radiactivo de un isótopo a lo largo de 10 años.
2. Un cajero automático (ATM) durante un día laborable.
3. Cálculo de la rentabilidad a largo plazo de una inversión con interés fijo garantizado del **5%** anual.
4. El tráfico de paquetes TCP/IP en un enrutador (Router) troncal.
5. El control de temperatura (termostato) de un horno industrial.
6. Un juego de ruleta en un casino tradicional.
7. Una línea de ensamblaje automatizada por robots que siempre tardan exactamente 5 segundos por pieza.
8. La trayectoria aerodinámica de un cohete en pleno lanzamiento.
9. El sistema de reserva de asientos de una aerolínea.
10. Un modelo para predecir el resultado de las elecciones presidenciales basado en encuestas.

---

## Resolución de la Práctica

| Sistema | Estático (E) / Dinámico (D) | Determinístico (Det) / Estocástico (Est) | Discreto (Disc) / Continuo (Cont) | Justificación Breve |
| :--- | :--- | :--- | :--- | :--- |
| **1. Decaimiento radiactivo** | D | Est | Cont | Evoluciona en el tiempo, es intrínsecamente probabilístico a nivel cuántico y la masa/energía decae de forma ininterrumpida. |
| **2. Cajero automático (ATM)** | D | Est | Disc | El tiempo avanza, las llegadas y tiempos de servicio son variables, y los clientes cambian el estado del sistema en eventos puntuales. |
| **3. Inversión con interés fijo** | D | Det | Disc | Evoluciona en el tiempo, el retorno es conocido y exacto, y el cálculo se aplica en periodos financieros definidos (mes/año). |
| **4. Tráfico TCP/IP en router** | D | Est | Disc | El volumen de red cambia con el tiempo, el comportamiento del usuario es impredecible y los paquetes llegan como unidades enteras. |
| **5. Control de temperatura** | D | Est | Cont | Cambia en el tiempo, sufre perturbaciones ambientales impredecibles y la temperatura fluctúa sin saltos abruptos. |
| **6. Ruleta de casino** | E | Est | Disc | El reloj no influye en la probabilidad de cada giro, el resultado depende del azar y los números de las casillas son finitos y exactos. |
| **7. Ensamblaje automatizado** | D | Det | Disc | El proceso avanza temporalmente, los robots no tienen variación en sus 5 segundos exactos, y las piezas terminan una por una. |
| **8. Trayectoria de cohete** | D | Det | Cont | Depende del reloj para la posición, se rige por ecuaciones físicas mecanicistas exactas, y su altura y velocidad cambian suavemente. |
| **9. Reserva de aerolínea** | D | Est | Disc | Ocurre a lo largo de un periodo, la demanda de compra es aleatoria y los asientos se ocupan por unidades enteras indivisibles. |
| **10. Predicción electoral** | E | Est | Disc | Es la fotografía estática de un momento específico, contiene un margen de error estadístico y contabiliza personas o votos enteros. |