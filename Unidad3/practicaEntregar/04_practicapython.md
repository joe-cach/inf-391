# Práctica 4: Pipeline Estocástico de Procesamiento de Pagos (Versión Python)

**Escenario de Estudio:** Microservicio de Pagos, API Antifraude y Gateway Bancario.
**Objetivo:** Modelar el ciclo de vida de 10,000 transacciones financieras utilizando Python y la librería `pandas`. Los estudiantes deberán aplicar la Transformada Inversa y lógica de ruteo estocástico mediante código puro, evitando el uso de generadores pre-construidos de NumPy para las distribuciones base.

---

## 1. Identificación y Reglas de la Arquitectura

1. **Llegada:** Los *payloads* de cobro llegan al microservicio desde el *frontend* de manera asíncrona.
2. **Clasificación (Bin):** El sistema extrae el BIN de la tarjeta de crédito para identificar la franquicia emisora.
3. **Validación Antifraude (API Externa):** El microservicio envía el *payload* a un proveedor de *Machine Learning* antifraude. Genera una latencia de red obligatoria en todos los casos.
4. **Veredicto:** El proveedor responde con un código de estado. Si se etiqueta como fraude, la transacción se bloquea (Drop) y no avanza.
5. **Autenticación (MFA):** Para transacciones válidas, el sistema evalúa qué nivel de seguridad 3D Secure exige el banco emisor.
6. **Liquidación Bancaria:** La transacción se envía al Gateway del banco para el cobro final, consumiendo hardware pesado antes de devolver el *Status 200 OK*.

---

## 2. Modelado Matemático (Input Modeling)

Deberán programar las siguientes 6 variables aleatorias desde cero (basándose en la generación de números uniformes `U = random.random()`):

*   **Continua 1: Llegadas de Transacciones (Exponencial)**
    *   *Parámetro:* Promedio de $\beta = 15$ ms.
    *   *Ecuación:* $T_{llegada} = -15 \cdot \ln(1 - U)$
*   **Discreta 1: Franquicia de la Tarjeta (Empírica)**
    *   *Regla:* $U \le 0.50 \implies$ "Visa". $0.50 < U \le 0.90 \implies$ "MasterCard". $U > 0.90 \implies$ "Amex".
*   **Continua 2: Latencia de API Antifraude (Uniforme Continua)**
    *   *Parámetros:* $a = 30$ ms, $b = 80$ ms.
    *   *Ecuación:* $T_{af} = 30 + U \cdot (80 - 30)$
*   **Discreta 2: Veredicto de Fraude (Bernoulli)**
    *   *Regla:* $U \le 0.92 \implies$ "Aprobado" (92%). Caso contrario $\implies$ "Fraude" (8%).
*   **Discreta 3: Requisito MFA (Empírica)**
    *   *Regla:* $U \le 0.60 \implies$ "Sin MFA". $0.60 < U \le 0.85 \implies$ "SMS". $U > 0.85 \implies$ "App Token".
*   **Continua 3: Tiempo de Liquidación Bancaria (Normal)**
    *   *Parámetros:* $\mu = 250$ ms, $\sigma = 30$ ms.
    *   *Implementación:* Utilizar la función nativa `random.normalvariate(mu, sigma)` o programar el algoritmo de Box-Muller.

---

## 3. Laboratorio Computacional en Python (Script Base)

Deben completar este *script* estructurando la lógica de control. El código recolecta los datos en una lista de diccionarios y usa `pandas` para replicar el análisis de salida que harían en Excel.

```python
import random
import math
import pandas as pd

# ==========================================
# 1. PARÁMETROS DEL SISTEMA
# ==========================================
BETA_LLEGADAS = 15.0
PROB_APROBADO = 0.92
AF_MIN, AF_MAX = 30.0, 80.0
BANCO_MU, BANCO_SIGMA = 250.0, 30.0
NUM_TRANSACCIONES = 10000

# ==========================================
# 2. MOTOR DE SIMULACIÓN MONTE CARLO
# ==========================================
logs_sistema = []
reloj_absoluto = 0.0

print(f"Iniciando simulación de {NUM_TRANSACCIONES} transacciones...")

for i in range(1, NUM_TRANSACCIONES + 1):
    # A. Variable Continua 1: Tiempo entre Llegadas (Exponencial)
    u_llegada = random.random()
    tiempo_entre_llegadas = -BETA_LLEGADAS * math.log(1 - u_llegada)
    reloj_absoluto += tiempo_entre_llegadas
    
    # B. Variable Discreta 1: Franquicia (Empírica)
    u_tarjeta = random.random()
    if u_tarjeta <= 0.50:
        franquicia = "Visa"
    elif u_tarjeta <= 0.90:
        franquicia = "MasterCard"
    else:
        franquicia = "Amex"
        
    # C. Variable Continua 2: Latencia API Antifraude (Uniforme)
    u_af = random.random()
    latencia_af = AF_MIN + u_af * (AF_MAX - AF_MIN)
    
    # D. Variable Discreta 2: Veredicto Antifraude (Bernoulli)
    u_fraude = random.random()
    if u_fraude <= PROB_APROBADO:
        estado_af = "Aprobado"
    else:
        estado_af = "Fraude"
        
    # LOGICA DE RUTEO: Si es fraude, bloqueamos el proceso y liberamos hardware
    if estado_af == "Fraude":
        tipo_mfa = "N/A"
        latencia_banco = 0.0
    else:
        # E. Variable Discreta 3: MFA (Empírica)
        u_mfa = random.random()
        if u_mfa <= 0.60:
            tipo_mfa = "Sin MFA"
        elif u_mfa <= 0.85:
            tipo_mfa = "SMS"
        else:
            tipo_mfa = "App Token"
            
        # F. Variable Continua 3: Liquidación (Normal)
        latencia_banco = random.normalvariate(BANCO_MU, BANCO_SIGMA)
    
    # Guardar el registro de la transacción
    logs_sistema.append({
        "ID_Tx": i,
        "Reloj_Llegada": reloj_absoluto,
        "Tiempo_Entre_Llegadas": tiempo_entre_llegadas,
        "Franquicia": franquicia,
        "Latencia_AF_ms": latencia_af,
        "Estado_Antifraude": estado_af,
        "Tipo_MFA": tipo_mfa,
        "Latencia_Banco_ms": latencia_banco
    })

# ==========================================
# 3. ANÁLISIS DE SALIDA (AUDITORÍA PANDAS)
# ==========================================
# Convertir a DataFrame (equivalente a la matriz de Excel)
df = pd.DataFrame(logs_sistema)

print("\n--- AUDITORÍA DE RESULTADOS (LEY DE LOS GRANDES NÚMEROS) ---")

# 1. Media de Llegadas (Debe tender a 15 ms)
media_llegadas = df['Tiempo_Entre_Llegadas'].mean()
print(f"Media de Llegadas (C1): {media_llegadas:.2f} ms (Esperado: {BETA_LLEGADAS})")

# 2. Porcentaje MasterCard (Debe tender al 40%)
tasa_mastercard = (len(df[df['Franquicia'] == 'MasterCard']) / NUM_TRANSACCIONES) * 100
print(f"Tasa MasterCard (D1): {tasa_mastercard:.1f}% (Esperado: 40.0%)")

# 3. Latencia Media AF (Debe tender a 55 ms)
media_af = df['Latencia_AF_ms'].mean()
esperado_af = (AF_MIN + AF_MAX) / 2
print(f"Latencia Media AF (C2): {media_af:.2f} ms (Esperado: {esperado_af})")

# 4. Tasa de Fraude (Debe tender al 8%)
tasa_fraude = (len(df[df['Estado_Antifraude'] == 'Fraude']) / NUM_TRANSACCIONES) * 100
esperado_fraude = (1 - PROB_APROBADO) * 100
print(f"Tasa de Fraude (D2): {tasa_fraude:.1f}% (Esperado: {esperado_fraude:.1f}%)")

# 5. Carga CPU Banco (Debe tender a 250 ms solo para los aprobados)
df_aprobados = df[df['Estado_Antifraude'] == 'Aprobado']
media_banco = df_aprobados['Latencia_Banco_ms'].mean()
print(f"Latencia Media Banco (C3): {media_banco:.2f} ms (Esperado: {BANCO_MU})")