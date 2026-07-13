# Práctica 1: Descomposición de Sistemas

## Escenarios de Estudio

1. **Sala de Urgencias Hospitalarias:** Pacientes que llegan con diferentes niveles de gravedad (triage) para ser atendidos por médicos y enfermeras.
2. **Intersección Vehicular:** Un cruce de dos avenidas principales controlado por un semáforo programable.
3. **Almacén de E-commerce:** Un centro de distribución donde ingresan productos de proveedores y salen pedidos despachados hacia clientes.

---

## Tabla de Descomposición de Sistemas

| Sistema | Entidades | Atributos (Ejemplo) | Actividades | Eventos | Variables de Estado (Ejemplo) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Urgencias** | Paciente, Médico | Gravedad del paciente | Examinar al paciente | Llegada de paciente | Cantidad de médicos libres |
| **Intersección** | Vehículo, Semáforo | Velocidad, Color actual del semáforo | Cruzar la calle, Esperar el verde | Cambio de luz, Llegada a la línea de pare | Vehículos esperando por carril, Estado del semáforo |
| **Almacén** | Pedido, Producto, Operario | Tamaño del pedido, Ubicación en estante | Buscar producto, Empaquetar pedido | Ingreso de orden al sistema, Despacho final | Pedidos en cola, Inventario disponible, Operarios libres |