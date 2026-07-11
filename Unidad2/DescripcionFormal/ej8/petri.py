import streamlit as st

# =====================================================================
# CONFIGURACIÓN GENERAL
# =====================================================================
st.set_page_config(page_title="Simulador PN - Productor Consumidor", layout="centered")

st.title("🏭 Simulador de Redes de Petri Clásicas")
st.write("### Desglose de la Tupla: $PN = (P, T, F, W, M_0)$")
st.write("**Caso:** Modelo Productor-Consumidor con Buffer Infinito.")
st.markdown("---")

# =====================================================================
# 1. MARCADO INICIAL (M_0)
# =====================================================================
st.header("1. Marcado Inicial ($M_0$)")
st.write("Representación del vector columna en el instante $t=0$.")

# Inicialización del vector de marcado
if "p1" not in st.session_state:
    st.session_state.p1 = 1  # Productor Listo
if "p2" not in st.session_state:
    st.session_state.p2 = 0  # Buffer
if "p3" not in st.session_state:
    st.session_state.p3 = 1  # Consumidor Listo

if "logs" not in st.session_state:
    st.session_state.logs = [
        "M_0 = [1, 0, 1]^T -> 1 Productor listo, 0 en Buffer, 1 Consumidor listo."
    ]

st.info("Vector de Arranque: $M_0 = \\begin{bmatrix} 1 \\\\ 0 \\\\ 1 \\end{bmatrix}$")
st.markdown("---")

# =====================================================================
# 2. VECTOR DE MARCADO ACTUAL (M_k)
# =====================================================================
st.header("2. Vector de Marcado Actual ($M_k$)")
st.write("Tokens (•) retenidos en cada lugar del sistema en tiempo real.")

col_p1, col_p2, col_p3 = st.columns(3)

with col_p1:
    st.subheader("Productor ($p_1$)")
    st.metric(label="• Listo para producir", value=st.session_state.p1)

with col_p2:
    st.subheader("Buffer ($p_2$)")
    st.metric(label="📦 • Datos en memoria", value=st.session_state.p2)

with col_p3:
    st.subheader("Consumidor ($p_3$)")
    st.metric(label="• Listo para consumir", value=st.session_state.p3)

st.markdown("---")

# =====================================================================
# 3. CONDICIÓN DE DISPARO / FACTIBILIDAD (Habilitación)
# =====================================================================
st.header("3. Habilitación de Transiciones ($\Gamma$)")
st.write("Una transición $t$ está habilitada si sus lugares de entrada ($Pre$) tienen los tokens necesarios.")

# Análisis de la matriz Pre
t1_hab = st.session_state.p1 >= 1
t2_hab = (st.session_state.p2 >= 1) and (st.session_state.p3 >= 1)

col_t1, col_t2 = st.columns(2)
with col_t1:
    st.success("🟢 Habilitada: t1 (Producir)" if t1_hab else "❌ Bloqueada: t1 (Producir)")
with col_t2:
    st.success("🟢 Habilitada: t2 (Consumir)" if t2_hab else "❌ Bloqueada: t2 (Consumir)")

st.markdown("---")

# =====================================================================
# 4. SIMULACIÓN DE DISPARO Y ECUACIÓN DE ESTADO (M_{k+1})
# =====================================================================
st.header("4. Simulación de Disparo de Eventos ($T$)")
st.write("Ejecuta la ecuación matricial $M_{k+1} = M_k + D \cdot u$")

def disparar_transicion(nombre, delta_p1, delta_p2, delta_p3):
    # Vector anterior Mk
    mk_str = f"[{st.session_state.p1}, {st.session_state.p2}, {st.session_state.p3}]^T"
    
    # Aplicación de la matriz D (Cambio neto)
    st.session_state.p1 += delta_p1
    st.session_state.p2 += delta_p2
    st.session_state.p3 += delta_p3
    
    # Vector nuevo Mk+1
    mk1_str = f"[{st.session_state.p1}, {st.session_state.p2}, {st.session_state.p3}]^T"
    
    vector_u = "[1, 0]^T" if nombre == "t1" else "[0, 1]^T"
    log = f"u = {vector_u} | M_k+1 = {mk_str} + D -> {mk1_str}"
    st.session_state.logs.insert(0, log)

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    st.write("**Ruta del Productor**")
    # Al disparar t1: p1 consume 1 y produce 1 (neto 0), p2 produce 1 (neto +1), p3 no interactúa (0)
    if st.button("Disparar t1 (Generar Dato)", disabled=not t1_hab, use_container_width=True):
        disparar_transicion("t1", delta_p1=0, delta_p2=1, delta_p3=0)
        st.rerun()

with col_btn2:
    st.write("**Ruta del Consumidor**")
    # Al disparar t2: p1 no interactúa (0), p2 consume 1 (neto -1), p3 consume 1 y produce 1 (neto 0)
    if st.button("Disparar t2 (Procesar Dato)", disabled=not t2_hab, use_container_width=True):
        disparar_transicion("t2", delta_p1=0, delta_p2=-1, delta_p3=0)
        st.rerun()

st.markdown("---")

# =====================================================================
# 5. CONSOLE AUDIT LOG
# =====================================================================
st.header("5. Historial de Ecuaciones de Estado ($M_{k+1}$)")
for log in st.session_state.logs[:8]:
    st.code(log, language="text")