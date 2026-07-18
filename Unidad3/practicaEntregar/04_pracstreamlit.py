import streamlit as st
import random
import math
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA STREAMLIT
# ==========================================
st.set_page_config(page_title="Simulador de Pagos", layout="wide")
st.title("💸 Pipeline Estocástico de Pagos")
st.markdown("Simulación de Monte Carlo con Eventos Asíncronos y Latencia de Red.")

# ==========================================
# 1. PARÁMETROS DEL SISTEMA (BARRA LATERAL)
# ==========================================
st.sidebar.header("⚙️ Parámetros del Sistema")
NUM_TRANSACCIONES = st.sidebar.number_input("Nº Transacciones", min_value=1000, max_value=100000, value=10000, step=1000)
BETA_LLEGADAS = st.sidebar.slider("Llegadas (Beta ms)", 1.0, 50.0, 15.0)
PROB_APROBADO = st.sidebar.slider("Prob. Aprobación AF", 0.0, 1.0, 0.92)

st.sidebar.subheader("Latencia Antifraude (Uniforme)")
AF_MIN = st.sidebar.number_input("Mínimo (ms)", value=30.0)
AF_MAX = st.sidebar.number_input("Máximo (ms)", value=80.0)

st.sidebar.subheader("Latencia Banco (Normal)")
BANCO_MU = st.sidebar.number_input("Media (μ ms)", value=250.0)
BANCO_SIGMA = st.sidebar.number_input("Desviación (σ ms)", value=30.0)

# ==========================================
# BOTÓN DE EJECUCIÓN
# ==========================================
if st.button("🚀 Ejecutar Simulación", type="primary"):
    
    # ==========================================
    # 2. MOTOR DE SIMULACIÓN MONTE CARLO
    # ==========================================
    logs_sistema = []
    reloj_absoluto = 0.0
    
    with st.spinner("Generando variables estocásticas..."):
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
                
            # LOGICA DE RUTEO
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
    # 3. ANÁLISIS DE SALIDA Y VISUALIZACIÓN
    # ==========================================
    df = pd.DataFrame(logs_sistema)
    
    st.success(f"Simulación de {NUM_TRANSACCIONES} transacciones completada con éxito.")
    
    # --- Pestañas de la UI ---
    tab1, tab2, tab3 = st.tabs(["Auditoría de Datos", "Reto de Laboratorio", "Base de Datos (Logs)"])
    
    with tab1:
        st.header("Auditoría de Resultados (Ley de los Grandes Números)")
        col1, col2, col3 = st.columns(3)
        
        # 1. Media de Llegadas
        media_llegadas = df['Tiempo_Entre_Llegadas'].mean()
        col1.metric("Media Llegadas (C1)", f"{media_llegadas:.2f} ms", f"Esperado: {BETA_LLEGADAS} ms")
        
        # 2. Latencia Media AF
        media_af = df['Latencia_AF_ms'].mean()
        esperado_af = (AF_MIN + AF_MAX) / 2
        col2.metric("Latencia Media AF (C2)", f"{media_af:.2f} ms", f"Esperado: {esperado_af} ms")
        
        # 3. Carga CPU Banco
        df_aprobados = df[df['Estado_Antifraude'] == 'Aprobado']
        media_banco = df_aprobados['Latencia_Banco_ms'].mean()
        col3.metric("Latencia Media Banco (C3)", f"{media_banco:.2f} ms", f"Esperado: {BANCO_MU} ms")
        
        st.divider()
        col4, col5 = st.columns(2)
        
        # 4. Tasa MasterCard
        tasa_mastercard = (len(df[df['Franquicia'] == 'MasterCard']) / NUM_TRANSACCIONES) * 100
        col4.metric("Tasa MasterCard (D1)", f"{tasa_mastercard:.1f}%", "Esperado: 40.0%")
        
        # 5. Tasa Fraude
        tasa_fraude = (len(df[df['Estado_Antifraude'] == 'Fraude']) / NUM_TRANSACCIONES) * 100
        esperado_fraude = (1 - PROB_APROBADO) * 100
        col5.metric("Tasa de Fraude (D2)", f"{tasa_fraude:.1f}%", f"Esperado: {esperado_fraude:.1f}%")

        # Gráfico visual de Fraudes
        st.subheader("Distribución de Estados Antifraude")
        st.bar_chart(df['Estado_Antifraude'].value_counts(), color="#FF4B4B")

    with tab2:
        st.header("Resultados del Reto de Laboratorio")
        # CORRECCIÓN AQUÍ: Agregamos la columna al df principal primero.
        df['Latencia_Total_ms'] = df['Latencia_AF_ms'] + df['Latencia_Banco_ms']
        
        # Reto 1
        media_total = df['Latencia_Total_ms'].mean()
        st.info(f"**1. Latencia Total Promedio:** {media_total:.2f} ms (Suma de AF y Banco)")
        
        # Reto 2
        tiempo_total_ms = df['Reloj_Llegada'].iloc[-1]
        tiempo_total_segundos = tiempo_total_ms / 1000
        st.info(f"**2. Tiempo Físico Simulado:** {tiempo_total_segundos:.2f} segundos para las {NUM_TRANSACCIONES} iteraciones.")
        
        # Reto 3
        costo_por_llamada_usd = 0.05
        cantidad_fraudes = len(df[df['Estado_Antifraude'] == 'Fraude'])
        costo_fraudes_usd = cantidad_fraudes * costo_por_llamada_usd
        st.error(f"**3. Costo Desperdiciado (API Fraude):** ${costo_fraudes_usd:.2f} USD")

        # Histograma de Latencia Total usando matplotlib
        st.subheader("Campana de Gauss: Latencia Total del Sistema")
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # CORRECCIÓN AQUÍ: Filtramos directamente sobre el df principal actualizado
        latencias_aprobadas = df[df['Estado_Antifraude'] == 'Aprobado']['Latencia_Total_ms']
        
        ax.hist(latencias_aprobadas, bins=50, color='skyblue', edgecolor='black')
        ax.set_title("Distribución de Latencias (Solo Tx Aprobadas)")
        ax.set_xlabel("Milisegundos (ms)")
        ax.set_ylabel("Frecuencia")
        st.pyplot(fig)

    with tab3:
        st.header("Matriz de Datos (Primeros 100 registros)")
        st.dataframe(df.head(100), use_container_width=True)
        st.caption("Los datos exportados representan el comportamiento de la memoria RAM del servidor.")