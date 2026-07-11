import streamlit as st

# =====================================================================
# CONFIGURACIÓN GENERAL
# =====================================================================
st.set_page_config(page_title="Simulador FSM Vectorial", layout="centered")

st.title("🚗 Simulador FSM Vectorial")
st.write("### Desglose explícito de la Tupla: $G = (S, E, f, \Gamma, s_0)$")
st.markdown("---")

# =====================================================================
# 1. ESTADO INICIAL (s_0)
# =====================================================================
st.header("1. Estado Inicial ($s_0$)")
st.write("Al encender el simulador, la memoria debe arrancar en un punto válido.")

if "Q" not in st.session_state:
    st.session_state.Q = 0
if "B1" not in st.session_state:
    st.session_state.B1 = 0
if "B2" not in st.session_state:
    st.session_state.B2 = 0
if "logs" not in st.session_state:
    st.session_state.logs = ["s_0 = (0, 0, 0) -> Fila vacía, bahías libres."]

st.info("El sistema arrancó en: $s_0 = (0, 0, 0)$")
st.markdown("---")

# =====================================================================
# 2. ESPACIO DE ESTADOS (S)
# =====================================================================
st.header("2. Estado Actual ($S$)")
st.write("El vector de memoria en este instante exacto de tiempo: $s = (Q, B_1, B_2)$")

estado_texto = {0: "Libre (0)", 1: "Ocupado: Rápido (1)", 2: "Ocupado: Completo (2)"}

col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.metric(label="Fila (Q)", value=f"{st.session_state.Q} / 5")
with col_s2:
    st.metric(label="Bahía 1 (B_1)", value=estado_texto[st.session_state.B1])
with col_s3:
    st.metric(label="Bahía 2 (B_2)", value=estado_texto[st.session_state.B2])

# Dibujo visual
cola_visual = "🚙 " * st.session_state.Q + "⬜ " * (5 - st.session_state.Q)
st.write(f"**Visualización:** [ {cola_visual} ]")
st.markdown("---")

# =====================================================================
# 3. FUNCIÓN DE FACTIBILIDAD (Gamma)
# =====================================================================
st.header("3. Función de Factibilidad ($\Gamma$)")
st.write("Evaluando el estado actual $s$, ¿qué eventos tienen permiso matemático de ocurrir?")

# Cálculos estrictos de Gamma
gamma_a = st.session_state.Q < 5
gamma_e1 = (st.session_state.Q > 0) and (st.session_state.B1 == 0)
gamma_e2 = (st.session_state.Q > 0) and (st.session_state.B2 == 0)
gamma_f1 = st.session_state.B1 != 0
gamma_f2 = st.session_state.B2 != 0

col_g1, col_g2 = st.columns(2)
with col_g1:
    st.success("✅ Permitido: Llegada ($a$)" if gamma_a else "❌ Bloqueado: Llegada ($a$)")
    st.success("✅ Permitido: Entrar B1 ($e_1$)" if gamma_e1 else "❌ Bloqueado: Entrar B1 ($e_1$)")
    st.success("✅ Permitido: Entrar B2 ($e_2$)" if gamma_e2 else "❌ Bloqueado: Entrar B2 ($e_2$)")
with col_g2:
    st.success("✅ Permitido: Terminar B1 ($f_1$)" if gamma_f1 else "❌ Bloqueado: Terminar B1 ($f_1$)")
    st.success("✅ Permitido: Terminar B2 ($f_2$)" if gamma_f2 else "❌ Bloqueado: Terminar B2 ($f_2$)")

st.markdown("---")

# =====================================================================
# 4. CONJUNTO DE EVENTOS (E)
# =====================================================================
st.header("4. Conjunto de Eventos ($E$)")
st.write("Los botones representan los estímulos externos. Solo están habilitados los que $\Gamma$ aprobó.")

def ejecutar_transicion(evento, nuevo_Q, nuevo_B1, nuevo_B2):
    s_antiguo = (st.session_state.Q, st.session_state.B1, st.session_state.B2)
    st.session_state.Q = nuevo_Q
    st.session_state.B1 = nuevo_B1
    st.session_state.B2 = nuevo_B2
    s_nuevo = (st.session_state.Q, st.session_state.B1, st.session_state.B2)
    
    # Registro de la Función f
    log = f"f( {s_antiguo}, {evento} ) = {s_nuevo}"
    st.session_state.logs.insert(0, log)

col_e1, col_e2, col_e3 = st.columns(3)

with col_e1:
    st.write("**Entradas ($a$)**")
    if st.button("Llegada ($a$)", disabled=not gamma_a, use_container_width=True):
        ejecutar_transicion("a", st.session_state.Q + 1, st.session_state.B1, st.session_state.B2)
        st.rerun()

with col_e2:
    st.write("**Asignaciones ($e$)**")
    if st.button("Entrar B1 Rápido ($e_{1R}$)", disabled=not gamma_e1, use_container_width=True):
        ejecutar_transicion("e_{1R}", st.session_state.Q - 1, 1, st.session_state.B2)
        st.rerun()
    if st.button("Entrar B1 Completo ($e_{1C}$)", disabled=not gamma_e1, use_container_width=True):
        ejecutar_transicion("e_{1C}", st.session_state.Q - 1, 2, st.session_state.B2)
        st.rerun()
    if st.button("Entrar B2 Rápido ($e_{2R}$)", disabled=not gamma_e2, use_container_width=True):
        ejecutar_transicion("e_{2R}", st.session_state.Q - 1, st.session_state.B1, 1)
        st.rerun()
    if st.button("Entrar B2 Completo ($e_{2C}$)", disabled=not gamma_e2, use_container_width=True):
        ejecutar_transicion("e_{2C}", st.session_state.Q - 1, st.session_state.B1, 2)
        st.rerun()

with col_e3:
    st.write("**Salidas ($f$)**")
    if st.button("Terminar B1 ($f_1$)", disabled=not gamma_f1, use_container_width=True):
        ejecutar_transicion("f_1", st.session_state.Q, 0, st.session_state.B2)
        st.rerun()
    if st.button("Terminar B2 ($f_2$)", disabled=not gamma_f2, use_container_width=True):
        ejecutar_transicion("f_2", st.session_state.Q, st.session_state.B1, 0)
        st.rerun()

st.markdown("---")

# =====================================================================
# 5. FUNCIÓN DE TRANSICIÓN DE ESTADOS (f)
# =====================================================================
st.header("5. Función de Transición ($f$)")
st.write("Auditoría de los cálculos aritméticos en la memoria del autómata:")

for log in st.session_state.logs[:8]:
    st.code(log, language="text")