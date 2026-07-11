import streamlit as st

# =====================================================================
# CONFIGURACIÓN GENERAL
# =====================================================================
st.set_page_config(page_title="Simulador FSM - Enrutador", layout="centered")

st.title("🌐 Simulador FSM Escalar Clásica")
st.write("### Desglose explícito de la Tupla: $G = (S, E, f, \Gamma, s_0)$")
st.write("**Caso:** Enrutador de red (1 CPU + Buffer de max 2 paquetes). Capacidad total = 3.")
st.markdown("---")

# =====================================================================
# 1. ESTADO INICIAL (s_0)
# =====================================================================
st.header("1. Estado Inicial ($s_0$)")
st.write("Al encender el equipo, tanto la CPU como el Buffer están completamente vacíos.")

if "S" not in st.session_state:
    st.session_state.S = 0  # S representa el total de paquetes en el sistema
if "logs" not in st.session_state:
    st.session_state.logs = ["s_0 = 0 -> Sistema iniciado (Vacío)."]

st.info("El sistema arrancó en: $s_0 = 0$")
st.markdown("---")

# =====================================================================
# 2. ESPACIO DE ESTADOS (S)
# =====================================================================
st.header("2. Estado Actual ($S$)")
st.write("La variable $s \in \{0, 1, 2, 3\}$ define la memoria del sistema.")

# Lógica de decodificación física a partir del estado escalar
cpu_ocupada = st.session_state.S > 0
paquetes_en_buffer = max(0, st.session_state.S - 1)

col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.metric(label="Estado Lógico (s)", value=f"{st.session_state.S} / 3")
with col_s2:
    st.metric(label="CPU", value="🔴 Ocupada" if cpu_ocupada else "🟢 Libre")
with col_s3:
    st.metric(label="Buffer", value=f"{paquetes_en_buffer} / 2")

# Representación visual del hardware
vis_cpu = "💻 [Paquete]" if cpu_ocupada else "💻 [Vacío]"
vis_buffer = "📦 " * paquetes_en_buffer + "⬜ " * (2 - paquetes_en_buffer)
st.write(f"**Hardware Visual:** CPU: `{vis_cpu}` | Buffer: `[ {vis_buffer} ]`")

if st.session_state.S == 3:
    st.error("⚠️ SISTEMA A MÁXIMA CAPACIDAD: El próximo paquete será descartado.")

st.markdown("---")

# =====================================================================
# 3. FUNCIÓN DE FACTIBILIDAD (Gamma)
# =====================================================================
st.header("3. Función de Factibilidad ($\Gamma$)")
st.write("Evaluando $s$, ¿qué eventos tienen permiso de procesarse?")

# La red externa siempre puede empujar datos (a), el equipo no puede impedirlo.
# Sin embargo, solo puede haber una salida (d) si hay algo en el sistema.
gamma_a = True 
gamma_d = st.session_state.S > 0

col_g1, col_g2 = st.columns(2)
with col_g1:
    st.success("✅ Físicamente Posible: Llegada ($a$)" if gamma_a else "❌ Bloqueado: Llegada ($a$)")
with col_g2:
    st.success("✅ Permitido: Salida ($d$)" if gamma_d else "❌ Bloqueado: Salida ($d$)")

st.markdown("---")

# =====================================================================
# 4. CONJUNTO DE EVENTOS (E)
# =====================================================================
st.header("4. Conjunto de Eventos ($E$)")
st.write("Inyecta los estímulos (Tráfico de Red).")

def ejecutar_transicion(evento):
    s_antiguo = st.session_state.S
    detalle = ""
    
    # Evaluación de la función de transición (f)
    if evento == "a":
        if s_antiguo < 3:
            st.session_state.S += 1
            detalle = "El paquete ingresó al nodo."
        else:
            # s se mantiene en 3. Esto es el DROP.
            detalle = "🛑 DROP: Buffer lleno, paquete destruido."
            
    elif evento == "d":
        st.session_state.S -= 1
        detalle = "El paquete terminó y abandonó el nodo."
        
    s_nuevo = st.session_state.S
    log = f"f({s_antiguo}, {evento}) = {s_nuevo} | {detalle}"
    st.session_state.logs.insert(0, log)

col_e1, col_e2 = st.columns(2)

with col_e1:
    if st.button("Llegada de Paquete ($a$)", disabled=not gamma_a, use_container_width=True):
        ejecutar_transicion("a")
        st.rerun()

with col_e2:
    if st.button("Salida de Paquete ($d$)", disabled=not gamma_d, use_container_width=True):
        ejecutar_transicion("d")
        st.rerun()

st.markdown("---")

# =====================================================================
# 5. FUNCIÓN DE TRANSICIÓN DE ESTADOS (f)
# =====================================================================
st.header("5. Función de Transición ($f$)")
st.write("Auditoría de la memoria escalar. Observa cómo $f(3, a) = 3$ refleja el descarte:")

for log in st.session_state.logs[:8]:
    st.code(log, language="text")