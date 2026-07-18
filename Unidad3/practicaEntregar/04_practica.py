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


# ==========================================
# 4. SOLUCIÓN AL RETO DE LABORATORIO
# ==========================================
print("\n--- RESULTADOS DEL RETO DE LABORATORIO ---")

# Reto 1: Latencia Total
df['Latencia_Total_ms'] = df['Latencia_AF_ms'] + df['Latencia_Banco_ms']
media_total = df['Latencia_Total_ms'].mean()
print(f"1. Latencia Total Promedio del Sistema: {media_total:.2f} ms")

# Reto 2: Tiempo Total Simulado (en segundos)
# Extraemos el reloj absoluto de la última fila (iloc[-1])
tiempo_total_ms = df['Reloj_Llegada'].iloc[-1]
tiempo_total_segundos = tiempo_total_ms / 1000
print(f"2. Tiempo Total Simulado: {tiempo_total_segundos:.2f} segundos para procesar las {NUM_TRANSACCIONES} transacciones.")

# Reto 3: Costo de Hardware (API) en transacciones de Fraude
costo_por_llamada_usd = 0.05
cantidad_fraudes = len(df[df['Estado_Antifraude'] == 'Fraude'])
costo_fraudes_usd = cantidad_fraudes * costo_por_llamada_usd
print(f"3. Costo de API desperdiciado en transacciones fraudulentas: ${costo_fraudes_usd:.2f} USD")