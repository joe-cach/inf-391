import streamlit as st

# =====================================================================
# CONFIGURACIÓN GENERAL
# =====================================================================
st.set_page_config(page_title="Simulador - Redes de Petri", layout="centered")

st.title("🕸️ Simulador de Redes de Petri")
st.write("### Desglose de la Tupla: $PN = (P, T, F, W, M_0)$")
st.write("**Caso:** Exclusión Mutua (Mutex) - Control de Recurso Compartido.")
st.markdown("---")

# =====================================================================
# 1. MARCADO INICIAL (M_0)
# =====================================================================
st.header("1. Marcado Inicial ($M_0$)")
st.write("Estado de los recursos y procesos al iniciar el sistema distribuidos en el conjunto de Lugares ($P$).")

# Inicialización de los lugares (Marcado de Tokens)
if "P1_Pensando" not in st.session_state:
    st.session_state.P1_Pensando = 1
if "P1_Esperando" not in st.session_state:
    st.session_state.P1_Esperando = 0
if "P1_Ejecutando" not in st.session_state:
    st.session_state.P1_Ejecutando = 0

if "Recurso_Semaf" not in st.session_state:
    st.session_state.Recurso_Semaf = 1 # Solo 1 token disponible (Mutex)

if "P2_Pensando" not in st.session_state:
    st.session_state.P2_Pensando = 1
if "P2_Esperando" not in st.session_state:
    st.session_state.P2_Esperando = 0
if "P2_Ejecutando" not in st.session_state:
    st.session_state.P2_Ejecutando = 0

if "logs" not in st.session_state:
    st.session_state.logs = ["M_0: Estado inicial precargado en la red."]

st.info("Marcado Inicial: Ambos procesos están 'Pensando' y el Recurso está disponible en el servidor.")
st.markdown("---")

# =====================================================================
# 2. VECTOR DE MARCADO ACTUAL (M_k)
# =====================================================================
st.header("2. Vector de Marcado Actual ($M_k$)")
st.write("Representación del número de tokens (•) retenidos en cada lugar en tiempo real.")

col_p1, col_r, col_p2 = st.columns(3)

with col_p1:
    st.subheader("Proceso 1")
    st.metric(label="• P1 Pensando", value=st.session_state.P1_Pensando)
    st.metric(label="• P1 Esperando", value=st.session_state.P1_Esperando)
    st.metric(label="• P1 Ejecutando", value=st.session_state.P1_Ejecutando)

with col_r:
    st.subheader("Servidor")
    st.metric(label="🔑 • Recurso Semáforo", value=st.session_state.Recurso_Semaf)

with col_p2:
    st.subheader("Proceso 2")
    st.metric(label="• P2 Pensando", value=st.session_state.P2_Pensando)
    st.metric(label="• P2 Esperando", value=st.session_state.P2_Esperando)
    st.metric(label="• P2 Ejecutando", value=st.session_state.P2_Ejecutando)

st.markdown("---")

# =====================================================================
# 3. CONDICIÓN DE DISPARO / FACTIBILIDAD (Habilitación de Transiciones)
# =====================================================================
st.header("3. Habilitación de Transiciones ($\Gamma$)")
st.write("Una transición $t$ está **habilitada** si todos sus lugares de entrada contienen al menos el peso del arco en tokens.")

# Lógica estricta de habilitación (En papel: Pre-condiciones)
t1_hab = st.session_state.P1_Pensando >= 1   # P1 quiere el recurso
t2_hab = (st.session_state.P1_Esperando >= 1) and (st.session_state.Recurso_Semaf >= 1) # Toma el recurso
t3_hab = st.session_state.P1_Ejecutando >= 1  # Libera el recurso

t4_hab = st.session_state.P2_Pensando >= 1   # P2 quiere el recurso
t5_hab = (st.session_state.P2_Esperando >= 1) and (st.session_state.Recurso_Semaf >= 1) # Toma el recurso
t6_hab = st.session_state.P2_Ejecutando >= 1  # Libera el recurso

col_th1, col_th2 = st.columns(2)
with col_th1:
    st.write("**Transiciones Proceso 1:**")
    st.success("🟢 t1 (P1 Solicitar)" if t1_hab else "❌ t1 (P1 Solicitar)")
    st.success("🟢 t2 (P1 Entrar a Recurso)" if t2_hab else "❌ t2 (P1 Entrar a Recurso)")
    st.success("🟢 t3 (P1 Terminar)" if t3_hab else "❌ t3 (P1 Terminar)")
with col_th2:
    st.write("**Transiciones Proceso 2:**")
    st.success("🟢 t4 (P2 Solicitar)" if t4_hab else "❌ t4 (P2 Solicitar)")
    st.success("🟢 t5 (P2 Entrar a Recurso)" if t5_hab else "❌ t5 (P2 Entrar a Recurso)")
    st.success("🟢 t6 (P2 Terminar)" if t6_hab else "❌ t6 (P2 Terminar)")

st.markdown("---")

# =====================================================================
# 4. CONJUNTO DE TRANSICIONES Y DINÁMICA DE DISPARO (f)
# =====================================================================

st.header("4. Simulación de Disparo de Eventos ($T$)")
st.write("Haz clic en una transición habilitada para consumir tokens de la entrada y depositarlos en la salida.")

def disparar_transicion(nombre, cambios):
    # 'cambios' es un diccionario que simula la suma/resta de la matriz de incidencia
    for lugar, valor in cambios.items():
        st.session_state[lugar] += valor
    
    log = f"Disparo de [{nombre}] -> Tokens reordenados en la matriz de red."
    st.session_state.logs.insert(0, log)

col_t1, col_t2 = st.columns(2)

with col_t1:
    st.write("**Acciones Proceso 1**")
    if st.button("Disparar t1 (P1 solicita)", disabled=not t1_hab, use_container_width=True):
        disparar_transicion("t1", {"P1_Pensando": -1, "P1_Esperando": 1})
        st.rerun()
    if st.button("Disparar t2 (P1 toma recurso)", disabled=not t2_hab, use_container_width=True):
        disparar_transicion("t2", {"P1_Esperando": -1, "Recurso_Semaf": -1, "P1_Ejecutando": 1})
        st.rerun()
    if st.button("Disparar t3 (P1 libera recurso)", disabled=not t3_hab, use_container_width=True):
        disparar_transicion("t3", {"P1_Ejecutando": -1, "Recurso_Semaf": 1, "P1_Pensando": 1})
        st.rerun()

with col_t2:
    st.write("**Acciones Proceso 2**")
    if st.button("Disparar t4 (P2 solicita)", disabled=not t4_hab, use_container_width=True):
        disparar_transicion("t4", {"P2_Pensando": -1, "P2_Esperando": 1})
        st.rerun()
    if st.button("Disparar t5 (P2 toma recurso)", disabled=not t5_hab, use_container_width=True):
        disparar_transicion("t5", {"P2_Esperando": -1, "Recurso_Semaf": -1, "P2_Ejecutando": 1})
        st.rerun()
    if st.button("Disparar t6 (P2 libera recurso)", disabled=not t6_hab, use_container_width=True):
        disparar_transicion("t6", {"P2_Ejecutando": -1, "Recurso_Semaf": 1, "P2_Pensando": 1})
        st.rerun()

st.markdown("---")

# =====================================================================
# 5. CONSOLE AUDIT LOG
# =====================================================================
st.header("5. Historial de Cambios de Marcado ($M_{k+1}$)")
for log in st.session_state.logs[:8]:
    st.code(log, language="text")