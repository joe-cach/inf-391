import streamlit as st

# =====================================================================
# CONFIGURACIÓN GENERAL
# =====================================================================
st.set_page_config(page_title="Simulador FSM - Planificador OS", layout="centered")

st.title("⚙️ Simulador FSM de Nodos Lógicos")
st.write("### Desglose explícito de la Tupla: $G = (S, E, f, \Gamma, s_0)$")
st.write("**Caso:** Ciclo de vida de un Proceso en el Sistema Operativo (Planificador).")
st.markdown("---")

# =====================================================================
# 1. ESTADO INICIAL (s_0)
# =====================================================================
st.header("1. Estado Inicial ($s_0$)")
st.write("Al hacer doble clic en un programa, el proceso nace obligatoriamente sin memoria asignada.")

if "S" not in st.session_state:
    st.session_state.S = "Nuevo"
if "logs" not in st.session_state:
    st.session_state.logs = ["s_0 = 'Nuevo' -> El usuario ejecutó el programa."]

st.info("El proceso arrancó en: $s_0 = \text{Nuevo}$")
st.markdown("---")

# =====================================================================
# 2. ESPACIO DE ESTADOS (S)
# =====================================================================
st.header("2. Estado Actual ($S$)")
st.write("El conjunto de nodos es $S = \{\text{Nuevo, Listo, En\_Ejecucion, En\_Espera, Terminado}\}$")

# Diccionario visual para la interfaz
estado_visual = {
    "Nuevo": "🐣 Nuevo (Creación)",
    "Listo": "📝 Listo (En RAM, esperando)",
    "En_Ejecucion": "🔥 En Ejecución (Usando CPU)",
    "En_Espera": "🧊 En Espera (Bloqueado por E/S)",
    "Terminado": "💀 Terminado (Destruido)"
}

st.metric(label="Fase de Vida Actual ($s$)", value=estado_visual[st.session_state.S])

if st.session_state.S == "Terminado":
    st.error("El proceso ha muerto. Sus datos fueron borrados de la memoria.")
    if st.button("🔄 Ejecutar un nuevo programa (Reiniciar)"):
        st.session_state.S = "Nuevo"
        st.session_state.logs = ["s_0 = 'Nuevo' -> Se lanzó un nuevo proceso."]
        st.rerun()

st.markdown("---")

# =====================================================================
# 3. FUNCIÓN DE FACTIBILIDAD (Gamma)
# =====================================================================
st.header("3. Función de Factibilidad ($\Gamma$)")
st.write("Evaluando el estado actual, ¿qué transiciones de sistema permite el Kernel?")

# Lógica estricta de Gamma basada en el estado actual
gamma_admitir = (st.session_state.S == "Nuevo")
gamma_despachar = (st.session_state.S == "Listo")
gamma_interrumpir = (st.session_state.S == "En_Ejecucion")
gamma_solicitar_io = (st.session_state.S == "En_Ejecucion")
gamma_salir = (st.session_state.S == "En_Ejecucion")
gamma_completar_io = (st.session_state.S == "En_Espera")

col_g1, col_g2 = st.columns(2)
with col_g1:
    st.success("✅ Admitir" if gamma_admitir else "❌ Admitir")
    st.success("✅ Despachar (CPU)" if gamma_despachar else "❌ Despachar (CPU)")
    st.success("✅ Interrumpir por Tiempo" if gamma_interrumpir else "❌ Interrumpir por Tiempo")
with col_g2:
    st.success("✅ Solicitar Hardware (E/S)" if gamma_solicitar_io else "❌ Solicitar Hardware (E/S)")
    st.success("✅ Completar Hardware (E/S)" if gamma_completar_io else "❌ Completar Hardware (E/S)")
    st.success("✅ Salir / Terminar" if gamma_salir else "❌ Salir / Terminar")

st.markdown("---")

# =====================================================================
# 4. CONJUNTO DE EVENTOS (E)
# =====================================================================
st.header("4. Conjunto de Eventos ($E$)")
st.write("Disparadores del sistema (Interrupciones de hardware o llamadas al sistema).")

def ejecutar_transicion(evento, estado_nuevo, detalle):
    estado_antiguo = st.session_state.S
    st.session_state.S = estado_nuevo
    log = f"f('{estado_antiguo}', {evento}) = '{estado_nuevo}' | {detalle}"
    st.session_state.logs.insert(0, log)

col_e1, col_e2 = st.columns(2)

with col_e1:
    if st.button("Admitir en RAM", disabled=not gamma_admitir, use_container_width=True):
        ejecutar_transicion("Admitir", "Listo", "Asignación de memoria exitosa.")
        st.rerun()
        
    if st.button("Despachar a CPU", disabled=not gamma_despachar, use_container_width=True):
        ejecutar_transicion("Despachar", "En_Ejecucion", "El Scheduler entrega el control al proceso.")
        st.rerun()
        
    if st.button("Interrupción de Reloj (Time-Slice)", disabled=not gamma_interrumpir, use_container_width=True):
        ejecutar_transicion("Interrumpir_Reloj", "Listo", "Tiempo agotado. Expulsado a la fila.")
        st.rerun()

with col_e2:
    if st.button("Solicitar Lectura (Bloqueo E/S)", disabled=not gamma_solicitar_io, use_container_width=True):
        ejecutar_transicion("Solicitar_IO", "En_Espera", "El proceso se congela esperando al disco.")
        st.rerun()
        
    if st.button("Completar Lectura (Fin E/S)", disabled=not gamma_completar_io, use_container_width=True):
        ejecutar_transicion("Completar_IO", "Listo", "El disco respondió. Vuelve a formarse en RAM.")
        st.rerun()
        
    if st.button("Salir (Terminar Tarea)", disabled=not gamma_salir, use_container_width=True):
        ejecutar_transicion("Salir", "Terminado", "Ejecución finalizada. Memoria liberada.")
        st.rerun()

st.markdown("---")

# =====================================================================
# 5. FUNCIÓN DE TRANSICIÓN DE ESTADOS (f)
# =====================================================================

st.header("5. Función de Transición ($f$)")
st.write("Auditoría del cambio de nodos lógicos del proceso:")

for log in st.session_state.logs[:10]:
    st.code(log, language="text")