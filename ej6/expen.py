import streamlit as st
import time

# =====================================================================
# CONFIGURACIÓN GENERAL
# =====================================================================
st.set_page_config(page_title="Simulador EFSM - Máquina Expendedora", layout="centered")

st.title("🧃 Simulador EFSM (Autómata Extendido)")
st.write("### Desglose explícito de la Tupla: $G_E = (S, E, V, \Gamma, f, s_0, v_0)$")
st.write("**Caso:** Máquina Expendedora interactiva con acumulador aritmético de crédito.")
st.markdown("---")

# =====================================================================
# 1. ESTADO INICIAL (s_0) Y MEMORIA INICIAL (v_0)
# =====================================================================
st.header("1. Arranque del Sistema ($s_0, v_0$)")
st.write("Al encenderse, la máquina limpia su memoria para evitar regalar dinero de sesiones anteriores.")

if "S" not in st.session_state:
    st.session_state.S = "Esperando_Cliente"  # s_0
if "credito" not in st.session_state:
    st.session_state.credito = 0              # v_0
if "logs" not in st.session_state:
    st.session_state.logs = ["Arranque: s_0='Esperando_Cliente' | v_0=(credito=0)"]

st.info("Arranque Exitoso: $s_0 = \text{Esperando\_Cliente} \quad | \quad v_0 = (\text{credito}: 0)$")
st.markdown("---")

# =====================================================================
# 2. ESPACIO DE ESTADOS (S) Y VARIABLES DE CONTEXTO (V)
# =====================================================================
st.header("2. Memoria Actual ($S$ y $V$)")
st.write("La máquina rastrea su fase operativa y mantiene el conteo exacto del dinero ingresado.")

col_s, col_v = st.columns(2)
with col_s:
    estado_ui = "🟢 Esperando Selección" if st.session_state.S == "Esperando_Cliente" else "⚙️ Despachando Producto"
    st.metric(label="Estado Lógico (S)", value=estado_ui)
with col_v:
    st.metric(label="Variable de Contexto (V): Crédito", value=f"{st.session_state.credito} Bs.")

st.markdown("---")

# =====================================================================
# 3. FUNCIÓN DE FACTIBILIDAD Y GUARDAS (Gamma)
# =====================================================================
st.header("3. Factibilidad y Guardas Lógicas ($\Gamma$)")
st.write("$\Gamma(s, v)$ evalúa si los botones deben estar activos basándose en el estado y el dinero acumulado.")

# Factibilidad de Estado
es_esperando = (st.session_state.S == "Esperando_Cliente")

# Evaluación de Guardas Lógicas basadas en V (credito)
guarda_cancelar = st.session_state.credito > 0
guarda_refresco = st.session_state.credito >= 5
guarda_agua = st.session_state.credito >= 3

col_g1, col_g2 = st.columns(2)
with col_g1:
    st.write("**Factibilidad por Estado:**")
    st.success("✅ Permitido: Insertar Moneda" if es_esperando else "❌ Bloqueado (Mecanismo Ocupado)")
with col_g2:
    st.write("**Evaluación de Guardas (Dinero):**")
    st.info(f"Cancelar [credito > 0] -> **{guarda_cancelar}**")
    st.info(f"Refresco [credito >= 5] -> **{guarda_refresco}**")
    st.info(f"Agua [credito >= 3] -> **{guarda_agua}**")

st.markdown("---")

# =====================================================================
# 4. CONJUNTO DE EVENTOS PARAMETRIZADOS (E)
# =====================================================================

st.header("4. Eventos Externos ($E$)")
st.write("Interactúa con la máquina introduciendo parámetros (monedas) o ejecutando acciones (botones).")

def ejecutar_transicion_extendida(evento, s_nuevo, credito_nuevo, guarda, accion):
    s_antiguo = st.session_state.S
    v_antiguo = f"credito={st.session_state.credito}"
    
    st.session_state.S = s_nuevo
    st.session_state.credito = credito_nuevo
    
    v_nuevo = f"credito={st.session_state.credito}"
    log = f"f('{s_antiguo}', {evento}, {v_antiguo}) | Guarda: [{guarda}] -> ('{s_nuevo}', {{{v_nuevo}}}) | {accion}"
    st.session_state.logs.insert(0, log)

if es_esperando:
    st.write("### 🪙 Ranura de Monedas (Acumulación)")
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        if st.button("Insertar Moneda (1 Bs.)", use_container_width=True):
            nuevo_credito = st.session_state.credito + 1
            ejecutar_transicion_extendida("Insertar_Moneda(1)", "Esperando_Cliente", nuevo_credito, "True", "Suma 1 al crédito.")
            st.rerun()
            
    with col_m2:
        if st.button("Insertar Moneda (2 Bs.)", use_container_width=True):
            nuevo_credito = st.session_state.credito + 2
            ejecutar_transicion_extendida("Insertar_Moneda(2)", "Esperando_Cliente", nuevo_credito, "True", "Suma 2 al crédito.")
            st.rerun()

    st.write("### 🎛️ Panel de Selección")
    col_b1, col_b2, col_b3 = st.columns(3)
    
    with col_b1:
        # El botón verifica la guarda localmente antes de ejecutar la acción
        if st.button("🥤 Refresco (5 Bs.)", use_container_width=True):
            if guarda_refresco:
                vuelto = st.session_state.credito - 5
                ejecutar_transicion_extendida("Seleccionar_Refresco", "Despachando", vuelto, "credito >= 5", f"Despacha bebida. Calcula vuelto: {vuelto} Bs.")
                st.rerun()
            else:
                st.error("❌ Guarda Fallida: Crédito insuficiente para Refresco.")
                
    with col_b2:
        if st.button("💧 Agua (3 Bs.)", use_container_width=True):
            if guarda_agua:
                vuelto = st.session_state.credito - 3
                ejecutar_transicion_extendida("Seleccionar_Agua", "Despachando", vuelto, "credito >= 3", f"Despacha bebida. Calcula vuelto: {vuelto} Bs.")
                st.rerun()
            else:
                st.error("❌ Guarda Fallida: Crédito insuficiente para Agua.")
                
    with col_b3:
        if st.button("🛑 Cancelar / Devolver", use_container_width=True):
            if guarda_cancelar:
                dinero_devuelto = st.session_state.credito
                ejecutar_transicion_extendida("Cancelar", "Esperando_Cliente", 0, "credito > 0", f"Devuelve billetes/monedas físicas por {dinero_devuelto} Bs.")
                st.success(f"💰 Se devolvieron {dinero_devuelto} Bs.")
                st.rerun()
            else:
                st.warning("No hay crédito para devolver.")

# =====================================================================
# SIMULACIÓN DEL EVENTO INTERNO AUTOMÁTICO (Hardware de Despacho)
# =====================================================================
if st.session_state.S == "Despachando":
    st.info("🔄 Mecanismo en movimiento. Por favor retire su producto (y vuelto si corresponde)...")
    
    # Simula el retraso mecánico de la máquina expendedora
    time.sleep(2.5) 
    
    # Evento de finalización automática (Transición interna)
    s_antiguo = "Despachando"
    v_antiguo = st.session_state.credito
    
    st.session_state.S = "Esperando_Cliente"
    st.session_state.credito = 0  # Limpieza post-venta
    
    log = f"f('{s_antiguo}', Fin_Despacho, credito={v_antiguo}) | Guarda: [True] -> ('Esperando_Cliente', {{credito=0}}) | Ciclo completado."
    st.session_state.logs.insert(0, log)
    st.rerun()

st.markdown("---")

# =====================================================================
# 5. FUNCIÓN DE TRANSICIÓN EXTENDIDA (f)
# =====================================================================
st.header("5. Función de Transición Extendida ($f$)")
st.write("Auditoría del cálculo de variables (Aritmética) y evaluación de las Guardas:")

for log in st.session_state.logs[:10]:
    st.code(log, language="text")