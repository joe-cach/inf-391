import streamlit as st

# =====================================================================
# CONFIGURACIÓN GENERAL
# =====================================================================
st.set_page_config(page_title="Simulador CPN - Auth API", layout="centered")

st.title("🔐 Simulador de Petri Coloreadas (CPN)")
st.write("### Desglose de la Tupla: $CPN = (\Sigma, P, T, A, N, C, G, E, I)$")
st.write("**Caso:** Servidor de Autenticación API (Enrutamiento JWT Premium vs Regular).")
st.markdown("---")

# =====================================================================
# 1. MARCADO INICIAL (M_0) Y DEFINICIÓN DE COLORES
# =====================================================================
st.header("1. Definición de Color ($\Sigma$) y Marcado Inicial ($M_0$)")
st.write("Los tokens son *Structs* de tipo `Peticion = {id: Int, tipo: String}`.")

# Inicialización de los lugares (Multiconjuntos de datos)
if "p1" not in st.session_state:
    # Buffer de entrada con 3 tokens estructurados
    st.session_state.p1 = [
        {"id": 101, "tipo": "REGULAR"},
        {"id": 102, "tipo": "PREMIUM"},
        {"id": 103, "tipo": "REGULAR"}
    ]
if "p2" not in st.session_state:
    st.session_state.p2 = [] # Fila Premium
if "p3" not in st.session_state:
    st.session_state.p3 = [] # Fila Regular

if "logs" not in st.session_state:
    st.session_state.logs = [
        "M_0: Buffer p1 inicializado con 3 peticiones JWT crudas."
    ]

if st.button("🔄 Reiniciar Escenario ($M_0$)"):
    st.session_state.p1 = [{"id": 101, "tipo": "REGULAR"}, {"id": 102, "tipo": "PREMIUM"}, {"id": 103, "tipo": "REGULAR"}]
    st.session_state.p2 = []
    st.session_state.p3 = []
    st.session_state.logs = ["M_0: Escenario reiniciado."]
    st.rerun()

st.markdown("---")

# =====================================================================
# 2. VECTOR DE MARCADO ACTUAL (M_k)
# =====================================================================
st.header("2. Estado de los Multiconjuntos ($M_k$)")
st.write("Inspección de la base de datos distribuida en tiempo real.")

col_p1, col_p2, col_p3 = st.columns(3)

with col_p1:
    st.subheader("Buffer ($p_1$)")
    if not st.session_state.p1:
        st.write("`∅ (Vacío)`")
    for tk in st.session_state.p1:
        st.code(f"{{id: {tk['id']}, tipo: {tk['tipo']}}}", language="json")

with col_p2:
    st.subheader("Fila VIP ($p_2$)")
    if not st.session_state.p2:
        st.write("`∅ (Vacío)`")
    for tk in st.session_state.p2:
        st.code(f"{{id: {tk['id']}, tipo: {tk['tipo']}}}", language="json")

with col_p3:
    st.subheader("Fila Std ($p_3$)")
    if not st.session_state.p3:
        st.write("`∅ (Vacío)`")
    for tk in st.session_state.p3:
        st.code(f"{{id: {tk['id']}, tipo: {tk['tipo']}}}", language="json")

st.markdown("---")

# =====================================================================
# 3. BINDING DE VARIABLES Y EVALUACIÓN DE GUARDAS (Gamma)
# =====================================================================
st.header("3. Asignación (*Binding*) y Guardas ($G$)")
st.write("En CPN, primero capturamos un token en la variable `req`, y luego el motor lógico evalúa si la guarda permite el paso.")

# Simulamos la selección de un token para evaluarlo
if st.session_state.p1:
    # El usuario elige qué token de la fila analizar (Binding)
    opciones_binding = {i: f"req = {{id: {tk['id']}, tipo: {tk['tipo']}}}" for i, tk in enumerate(st.session_state.p1)}
    seleccion_idx = st.selectbox("Selecciona un token del Buffer para evaluarlo:", options=list(opciones_binding.keys()), format_func=lambda x: opciones_binding[x])
    
    # Token actual asignado a la variable 'req'
    req = st.session_state.p1[seleccion_idx]
    
    # Evaluación de Guardas
    guarda_t1 = (req["tipo"] == "PREMIUM")
    guarda_t2 = (req["tipo"] == "REGULAR")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.write("**Transición $t_1$ (Ruta Premium)**")
        st.info(f"$G(t_1): [\\text{{req.tipo}} == \\text{{PREMIUM}}]$")
        st.success("🟢 Habilitada" if guarda_t1 else "❌ Bloqueada")
        
    with col_g2:
        st.write("**Transición $t_2$ (Ruta Regular)**")
        st.info(f"$G(t_2): [\\text{{req.tipo}} == \\text{{REGULAR}}]$")
        st.success("🟢 Habilitada" if guarda_t2 else "❌ Bloqueada")

else:
    st.warning("El Buffer $p_1$ está vacío. No hay tokens para asignar a la variable `req`.")
    req = None
    guarda_t1 = False
    guarda_t2 = False

st.markdown("---")

# =====================================================================
# 4. SIMULACIÓN DE DISPARO Y ENRUTAMIENTO
# =====================================================================
st.header("4. Ejecución del Enrutador Lógico ($T$)")

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("Disparar t1 (Clasificar como VIP)", disabled=not guarda_t1, use_container_width=True):
        # 1. Extraer del multiconjunto de origen
        st.session_state.p1.pop(seleccion_idx)
        # 2. Insertar en el multiconjunto de destino
        st.session_state.p2.append(req)
        
        log = f"Disparo t1 | req={req['id']} | G(t1) = True -> Movido a Fila VIP (p2)."
        st.session_state.logs.insert(0, log)
        st.rerun()

with col_btn2:
    if st.button("Disparar t2 (Clasificar como Std)", disabled=not guarda_t2, use_container_width=True):
        st.session_state.p1.pop(seleccion_idx)
        st.session_state.p3.append(req)
        
        log = f"Disparo t2 | req={req['id']} | G(t2) = True -> Movido a Fila Std (p3)."
        st.session_state.logs.insert(0, log)
        st.rerun()

st.markdown("---")

# =====================================================================
# 5. CONSOLE AUDIT LOG
# =====================================================================
st.header("5. Historial de Enrutamiento (Logs)")
for log in st.session_state.logs[:8]:
    st.code(log, language="text")