import streamlit as st
import time

# =====================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILO VISUAL
# =====================================================================
st.set_page_config(page_title="Simulador EFSM - Expendedora", layout="centered")

st.title("🤖 Simulador Interactivo EFSM")
st.subheader("Materia: Simulación de Sistemas - Caso: Máquina Expendedora")
st.write("Estudio formal de la tupla: $G_E = (S, E, V, \Gamma, f, s_0, v_0)$")
st.markdown("---")

# =====================================================================
# 2. INICIALIZACIÓN DEL ESTADO DE MEMORIA (Constructor v0 y s0)
# =====================================================================
# Streamlit se ejecuta de arriba a abajo en cada clic. 
# Usamos 'session_state' para mantener la memoria RAM del autómata persistente.
if "estado_logico" not in st.session_state:
    st.session_state.estado_logico = "Esperando_Cliente"  # s0
if "credito" not in st.session_state:
    st.session_state.credito = 0  # v0
if "logs" not in st.session_state:
    st.session_state.logs = ["v0 & s0: Sistema inicializado en Esperando_Cliente con Credito = 0 Bs."]

# Función auxiliar para registrar las transiciones matemáticas f(s, e, v)
def registrar_log(evento, estado_antiguo, estado_nuevo, credito_antiguo, credito_nuevo, guarda="True", accion="Ninguna"):
    log = f"f({estado_antiguo}, {evento}, Credito={credito_antiguo}Bs) | Guardas: [{guarda}] -> ({estado_nuevo}, {{credito={credito_nuevo}Bs}}) | Acción: {accion}"
    st.session_state.logs.insert(0, log)

# =====================================================================
# 3. PANEL DE CONTROL SUPERIOR (Visualización del Estado Actual)
# =====================================================================
col_s, col_v = st.columns(2)
with col_s:
    st.metric(label="Estado Lógico Actual (S)", value=st.session_state.estado_logico)
with col_v:
    st.metric(label="Variable de Contexto (V) - Crédito", value=f"{st.session_state.credito} Bs")

# Renderizado visual dinámico de las pantallas de la máquina
if st.session_state.estado_logico == "Esperando_Cliente":
    st.info("📺 PANTALLA: Introduzca monedas o seleccione su bebida.")
elif st.session_state.estado_logico == "Despachando":
    st.warning("🔄 MECANISMO: Despachando bebida y calculando vuelto... Por favor espere.")

st.markdown("---")

# =====================================================================
# 4. INTERFAZ DE HARDWARE (Botones de Eventos E)
# =====================================================================
st.write("### 🎛️ Panel de Interacción (Eventos Externos)")

# Deshabilitar botones si la máquina está ocupada despachando (Función de Factibilidad Gamma)
bloqueado = st.session_state.estado_logico == "Despachando"

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🪙 Moneda 1 Bs", disabled=bloqueado):
        s_antiguo = st.session_state.estado_logico
        v_antiguo = st.session_state.credito
        
        # Función de Transición f: Al introducir moneda, el crédito aumenta
        st.session_state.credito += 1
        registrar_log("Insertar_Moneda(1)", s_antiguo, s_antiguo, v_antiguo, st.session_state.credito, accion="credito = credito + 1")
        st.rerun()

with col2:
    if st.button("🪙 Moneda 2 Bs", disabled=bloqueado):
        s_antiguo = st.session_state.estado_logico
        v_antiguo = st.session_state.credito
        
        st.session_state.credito += 2
        registrar_log("Insertar_Moneda(2)", s_antiguo, s_antiguo, v_antiguo, st.session_state.credito, accion="credito = credito + 2")
        st.rerun()

with col3:
    if st.button("🥤 Refresco (5Bs)", disabled=bloqueado):
        s_antiguo = st.session_state.estado_logico
        v_antiguo = st.session_state.credito
        
        # EVALUACIÓN DE GUARDAS LÓGICAS (Gamma)
        if st.session_state.credito >= 5:
            vuelto = st.session_state.credito - 5
            st.session_state.credito = vuelto
            st.session_state.estado_logico = "Despachando"
            registrar_log("Seleccionar_Refresco", s_antiguo, "Despachando", v_antiguo, st.session_state.credito, guarda="credito >= 5", accion=f"Despachar Refresco. Vuelto: {vuelto} Bs")
            st.rerun()
        else:
            st.error("❌ Guarda Fallida: Crédito insuficiente para comprar Refresco (Requiere 5 Bs).")
            st.session_state.logs.insert(0, f"⚠️ EVENTO BLOQUEADO: Seleccionar_Refresco | Guarda [credito >= 5] evaluada como FALSO.")

with col4:
    if st.button("💧 Agua (3Bs)", disabled=bloqueado):
        s_antiguo = st.session_state.estado_logico
        v_antiguo = st.session_state.credito
        
        # EVALUACIÓN DE GUARDAS LÓGICAS (Gamma)
        if st.session_state.credito >= 3:
            vuelto = st.session_state.credito - 3
            st.session_state.credito = vuelto
            st.session_state.estado_logico = "Despachando"
            registrar_log("Seleccionar_Agua", s_antiguo, "Despachando", v_antiguo, st.session_state.credito, guarda="credito >= 3", accion=f"Despachar Agua. Vuelto: {vuelto} Bs")
            st.rerun()
        else:
            st.error("❌ Guarda Fallida: Crédito insuficiente para comprar Agua (Requiere 3 Bs).")
            st.session_state.logs.insert(0, f"⚠️ EVENTO BLOQUEADO: Seleccionar_Agua | Guarda [credito >= 3] evaluada como FALSO.")

with col5:
    if st.button("🚨 Cancelar", disabled=bloqueado):
        s_antiguo = st.session_state.estado_logico
        v_antiguo = st.session_state.credito
        
        if st.session_state.credito > 0:
            st.session_state.credito = 0
            registrar_log("Cancelar", s_antiguo, s_antiguo, v_antiguo, 0, guarda="credito > 0", accion=f"Devolviendo {v_antiguo} Bs físicos")
            st.success(f"💰 Se han devuelto tus {v_antiguo} Bs.")
            st.rerun()
        else:
            st.session_state.logs.insert(0, f"⚠️ EVENTO IGNORADO: Cancelar | Guarda [credito > 0] evaluada como FALSO.")

# =====================================================================
# 5. SIMULACIÓN DEL EVENTO INTERNO AUTOMÁTICO (Fin_Despacho)
# =====================================================================
if st.session_state.estado_logico == "Despachando":
    # Simulamos el tiempo físico que tardan los engranajes mecánicos en soltar la lata
    with st.spinner("Entregando producto..."):
        time.sleep(2.5)  # Demora de simulación
    
    s_antiguo = st.session_state.estado_logico
    v_antiguo = st.session_state.credito
    
    # Transición automática de regreso al estado de reposo
    st.session_state.estado_logico = "Esperando_Cliente"
    st.session_state.credito = 0
    registrar_log("Fin_Despacho", s_antiguo, "Esperando_Cliente", v_antiguo, 0, accion="Motores apagados. Crédito reiniciado.")
    st.balloons()  # Animación festiva de entrega exitosa
    st.rerun()

# =====================================================================
# 6. HISTORIAL DE LOGS MATEMÁTICOS (Auditoría de la Tupla)
# =====================================================================
st.markdown("---")
st.write("### 📜 Consola de Transición de la EFSM (Historial del Motor)")
for log in st.session_state.logs[:8]:  # Mostrar los últimos 8 eventos
    st.code(log, language="text")