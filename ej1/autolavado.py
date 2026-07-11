import streamlit as st

# =====================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# =====================================================================
st.set_page_config(page_title="Simulador FSM Vectorial - Autolavado", layout="centered")

st.title("🚗 Simulador Interactivo FSM Vectorial")
st.subheader("Materia: Simulación de Sistemas - Caso: Autolavado")
st.write("Estudio formal de la tupla: G = (S, E, f, Γ, s0)")
st.markdown("---")

# =====================================================================
# 2. INICIALIZACIÓN DEL ESPACIO DE ESTADOS (Constructor s0)
# =====================================================================
# El vector de estado es S = (Q, B1, B2)
# s0 = (0, 0, 0) -> Fila vacía, ambas bahías libres.

if "Q" not in st.session_state:
    st.session_state.Q = 0  # Autos en fila (Máximo 5)
if "B1" not in st.session_state:
    st.session_state.B1 = 0 # 0=Libre, 1=Rápido, 2=Completo
if "B2" not in st.session_state:
    st.session_state.B2 = 0 # 0=Libre, 1=Rápido, 2=Completo
if "logs" not in st.session_state:
    st.session_state.logs = ["s0: Sistema inicializado en el vector (0, 0, 0)"]

def registrar_log(evento, s_antiguo, s_nuevo, detalle=""):
    log = f"f({s_antiguo}, {evento}) = {s_nuevo} | {detalle}"
    st.session_state.logs.insert(0, log)

# Diccionario para traducir los números lógicos a texto para la interfaz
estado_texto = {0: "🟩 Libre", 1: "🟧 Lavado Rápido", 2: "🟥 Lavado Completo"}

# =====================================================================
# 3. PANEL DE CONTROL SUPERIOR (Visualización del Vector Actual)
# =====================================================================
st.write("### 📊 Vector de Estado Actual: $S = (Q, B_1, B_2)$")

col_q, col_b1, col_b2 = st.columns(3)
with col_q:
    st.metric(label="Fila de Espera (Q)", value=f"{st.session_state.Q} / 5 Autos")
with col_b1:
    st.metric(label="Bahía 1 (B1)", value=estado_texto[st.session_state.B1])
with col_b2:
    st.metric(label="Bahía 2 (B2)", value=estado_texto[st.session_state.B2])

# Dibujo visual de la fila
cola_visual = "🚙 " * st.session_state.Q + "⬜ " * (5 - st.session_state.Q)
st.info(f"**Visualización de la Fila:** [ {cola_visual} ]")

st.markdown("---")

# =====================================================================
# 4. INTERFAZ DE EVENTOS Y FUNCIÓN DE FACTIBILIDAD (Gamma)
# =====================================================================
st.write("### 🎛️ Panel de Eventos (Disparadores de Transición)")

# --- EVENTO EXTERNO: LLEGADA ---
st.write("**1. Tráfico Externo**")
# Gamma(Llegada): Físicamente un auto siempre puede llegar, pero si Q=5, lo descartamos (Drop)
if st.button("Llegada de Auto (a)", use_container_width=True):
    s_antiguo = (st.session_state.Q, st.session_state.B1, st.session_state.B2)
    if st.session_state.Q < 5:
        st.session_state.Q += 1
        s_nuevo = (st.session_state.Q, st.session_state.B1, st.session_state.B2)
        registrar_log("a", s_antiguo, s_nuevo, "Auto entra a la fila.")
    else:
        # Política de Descarte (Drop)
        registrar_log("a", s_antiguo, s_antiguo, "⚠️ DROP: Fila llena. Cliente rechazado.")
        st.error("¡Descarte! El autolavado está a máxima capacidad.")
    st.rerun()

st.write("**2. Asignación a Bahías**")
col_asig1, col_asig2 = st.columns(2)

# Gamma: Solo se puede asignar si hay alguien en la fila (Q > 0) y la bahía está libre (B = 0)
puede_entrar_b1 = (st.session_state.Q > 0) and (st.session_state.B1 == 0)
puede_entrar_b2 = (st.session_state.Q > 0) and (st.session_state.B2 == 0)

with col_asig1:
    if st.button("Entrar B1: Rápido (e_1R)", disabled=not puede_entrar_b1, use_container_width=True):
        s_antiguo = (st.session_state.Q, st.session_state.B1, st.session_state.B2)
        st.session_state.Q -= 1
        st.session_state.B1 = 1
        s_nuevo = (st.session_state.Q, st.session_state.B1, st.session_state.B2)
        registrar_log("e_1R", s_antiguo, s_nuevo, "Auto sale de fila y entra a B1 (Rápido).")
        st.rerun()
        
    if st.button("Entrar B1: Completo (e_1C)", disabled=not puede_entrar_b1, use_container_width=True):
        s_antiguo = (st.session_state.Q, st.session_state.B1, st.session_state.B2)
        st.session_state.Q -= 1
        st.session_state.B1 = 2
        s_nuevo = (st.session_state.Q, st.session_state.B1, st.session_state.B2)
        registrar_log("e_1C", s_antiguo, s_nuevo, "Auto sale de fila y entra a B1 (Completo).")
        st.rerun()

with col_asig2:
    if st.button("Entrar B2: Rápido (e_2R)", disabled=not puede_entrar_b2, use_container_width=True):
        s_antiguo = (st.session_state.Q, st.session_state.B1, st.session_state.B2)
        st.session_state.Q -= 1
        st.session_state.B2 = 1
        s_nuevo = (st.session_state.Q, st.session_state.B1, st.session_state.B2)
        registrar_log("e_2R", s_antiguo, s_nuevo, "Auto sale de fila y entra a B2 (Rápido).")
        st.rerun()
        
    if st.button("Entrar B2: Completo (e_2C)", disabled=not puede_entrar_b2, use_container_width=True):
        s_antiguo = (st.session_state.Q, st.session_state.B1, st.session_state.B2)
        st.session_state.Q -= 1
        st.session_state.B2 = 2
        s_nuevo = (st.session_state.Q, st.session_state.B1, st.session_state.B2)
        registrar_log("e_2C", s_antiguo, s_nuevo, "Auto sale de fila y entra a B2 (Completo).")
        st.rerun()

st.write("**3. Fin de Servicio (Salida)**")
col_fin1, col_fin2 = st.columns(2)

# Gamma: Solo se puede terminar un lavado si la bahía está ocupada (B != 0)
puede_terminar_b1 = (st.session_state.B1 != 0)
puede_terminar_b2 = (st.session_state.B2 != 0)

with col_fin1:
    if st.button("Terminar B1 (f_1)", disabled=not puede_terminar_b1, use_container_width=True):
        s_antiguo = (st.session_state.Q, st.session_state.B1, st.session_state.B2)
        st.session_state.B1 = 0
        s_nuevo = (st.session_state.Q, st.session_state.B1, st.session_state.B2)
        registrar_log("f_1", s_antiguo, s_nuevo, "Bahía 1 finaliza y se libera.")
        st.rerun()

with col_fin2:
    if st.button("Terminar B2 (f_2)", disabled=not puede_terminar_b2, use_container_width=True):
        s_antiguo = (st.session_state.Q, st.session_state.B1, st.session_state.B2)
        st.session_state.B2 = 0
        s_nuevo = (st.session_state.Q, st.session_state.B1, st.session_state.B2)
        registrar_log("f_2", s_antiguo, s_nuevo, "Bahía 2 finaliza y se libera.")
        st.rerun()

# =====================================================================
# 5. HISTORIAL LÓGICO
# =====================================================================
st.markdown("---")
st.write("### 📜 Consola de Transiciones Vectoriales")
for log in st.session_state.logs[:10]:
    st.code(log, language="text")