import streamlit as st

# =====================================================================
# CONFIGURACIÓN GENERAL
# =====================================================================
st.set_page_config(page_title="Simulador FSM - Sistema de Alarma", layout="centered")

st.title("🚨 Simulador FSM de Nodos Lógicos")
st.write("### Desglose explícito de la Tupla: $G = (S, E, f, \Gamma, s_0)$")
st.write("**Caso:** Sistema de Alarma Residencial con Modo de Preparación e Interrupción Global.")
st.markdown("---")

# =====================================================================
# 1. ESTADO INICIAL (s_0)
# =====================================================================
st.header("1. Estado Inicial ($s_0$)")
st.write("Por motivos de seguridad y prevención de falsos positivos en reinicios eléctricos, el sistema arranca apagado.")

if "S" not in st.session_state:
    st.session_state.S = "Desarmado"  # s_0
if "logs" not in st.session_state:
    st.session_state.logs = ["s_0 = 'Desarmado' -> Panel encendido en modo seguro (Reposo)."]

st.info("El sistema arrancó en: $s_0 = \text{Desarmado}$")
st.markdown("---")

# =====================================================================
# 2. ESPACIO DE ESTADOS (S)
# =====================================================================
st.header("2. Estado Actual ($S$)")
st.write("El conjunto finito de modos operativos excluyentes es $S = \{\text{Desarmado, Armandose, Armado, Sirena}\}$")

# Mapeo visual y alertas dinámicas según la fase operativa
estado_visual = {
    "Desarmado": "🟢 Desarmado (Libre tránsito)",
    "Armandose": "⏳ Armándose (Temporizador de salida activo)",
    "Armado": "🔒 Armado (Vigilancia activa de sensores)",
    "Sirena": "🔊 SIRENA ACTIVADA (¡Alerta de Intruso!)"
}

if st.session_state.S == "Sirena":
    st.error(f"ESTADO ACTUAL: {estado_visual[st.session_state.S]}")
elif st.session_state.S == "Armandose":
    st.warning(f"ESTADO ACTUAL: {estado_visual[st.session_state.S]}")
else:
    st.success(f"ESTADO ACTUAL: {estado_visual[st.session_state.S]}")

st.markdown("---")

# =====================================================================
# 3. FUNCIÓN DE FACTIBILIDAD (Gamma)
# =====================================================================
st.header("3. Función de Factibilidad ($\Gamma$)")
st.write("Filtro de seguridad lógica: ¿Qué estímulos del entorno físico permite procesar el estado actual $s$?")

# Lógica estricta de Gamma
gamma_clave = True # La clave correcta siempre es factible y tiene máxima prioridad (Regla 5)
gamma_tiempo = (st.session_state.S == "Armandose")
gamma_movimiento = (st.session_state.S == "Armado")

col_g1, col_g2 = st.columns(2)
with col_g1:
    st.success("✅ Clave_Correcta (Siempre disponible)")
    st.success("✅ Permitido: Tiempo_Expirado" if gamma_tiempo else "❌ Bloqueado: Tiempo_Expirado")
with col_g2:
    st.success("✅ Permitido: Deteccion_Movimiento" if gamma_movimiento else "❌ Bloqueado: Deteccion_Movimiento")

st.markdown("---")

# =====================================================================
# 4. CONJUNTO DE EVENTOS (E)
# =====================================================================
st.header("4. Conjunto de Eventos ($E$)")
st.write("Interactúa con el entorno de la vivienda disparando eventos.")

def ejecutar_transicion(evento, estado_nuevo, detalle):
    estado_antiguo = st.session_state.S
    st.session_state.S = estado_nuevo
    log = f"f('{estado_antiguo}', {evento}) = '{estado_nuevo}' | {detalle}"
    st.session_state.logs.insert(0, log)

col_e1, col_e2, col_e3 = st.columns(3)

with col_e1:
    st.write("**Interfaz de Usuario**")
    if st.button("Ingresar Clave Correcta", disabled=not gamma_clave, use_container_width=True):
        if st.session_state.S == "Desarmado":
            # Inicia cuenta regresiva
            ejecutar_transicion("Clave_Correcta", "Armandose", "Inicia temporizador de 30s para salir.")
        else:
            # Regla de interrupción global: Volver a desarmado desde cualquier nodo
            ejecutar_transicion("Clave_Correcta", "Desarmado", "Código válido. Panel desactivado de inmediato.")
        st.rerun()

with col_e2:
    st.write("**Eventos de Reloj**")
    if st.button("Simular Expira Tiempo (30s)", disabled=not gamma_tiempo, use_container_width=True):
        ejecutar_transicion("Tiempo_Expirado", "Armado", "Tiempo de gracia agotado. Sensores encendidos.")
        st.rerun()

with col_e3:
    st.write("**Sensores del Entorno**")
    if st.button("Sensor: Detectar Movimiento", disabled=not gamma_movimiento, use_container_width=True):
        ejecutar_transicion("Deteccion_Movimiento", "Sirena", "¡Sensor violado! Activando sirena de alta potencia.")
        st.rerun()

st.markdown("---")

# =====================================================================
# 5. FUNCIÓN DE TRANSICIÓN DE ESTADOS (f)
# =====================================================================
st.header("5. Función de Transición ($f$)")
st.write("Auditoría de cambios de modo. Analiza la consistencia matemática del Kernel de seguridad:")

for log in st.session_state.logs[:8]:
    st.code(log, language="text")