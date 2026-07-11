import streamlit as st

# =====================================================================
# CONFIGURACIÓN GENERAL
# =====================================================================
st.set_page_config(page_title="Simulador EFSM - Cajero ATM", layout="centered")

st.title("💳 Simulador EFSM (Autómata Extendido)")
st.write("### Desglose explícito de la Tupla: $G_E = (S, E, V, \Gamma, f, s_0, v_0)$")
st.write("**Caso:** Cajero Automático (ATM) con validación de seguridad y control de saldo.")
st.markdown("---")

# =====================================================================
# 1. ESTADO INICIAL (s_0) Y MEMORIA INICIAL (v_0)
# =====================================================================
st.header("1. Arranque del Sistema ($s_0, v_0$)")
st.write("Al ingresar la tarjeta, el sistema arranca en un nodo lógico y precarga sus variables locales.")

# Inicialización persistente
if "S" not in st.session_state:
    st.session_state.S = "Autenticando"  # s_0
if "intentos" not in st.session_state:
    st.session_state.intentos = 0        # v_0 (Variable 1)
if "saldo" not in st.session_state:
    st.session_state.saldo = 5000.0      # v_0 (Variable 2: Simula consulta a BD)
if "logs" not in st.session_state:
    st.session_state.logs = ["Arranque: s_0='Autenticando' | v_0=(intentos=0, saldo=5000)"]

st.info("Arranque Exitoso: $s_0 = \text{Autenticando} \quad | \quad v_0 = (\text{intentos}: 0, \text{saldo}: 5000)$")
st.markdown("---")

# =====================================================================
# 2. ESPACIO DE ESTADOS (S) Y VARIABLES DE CONTEXTO (V)
# =====================================================================
st.header("2. Memoria Actual ($S$ y $V$)")
st.write("A diferencia de la FSM pura, aquí rastreamos la pantalla actual ($S$) y el estado de la RAM ($V$).")

col_s, col_v1, col_v2 = st.columns(3)
with col_s:
    st.metric(label="Estado Lógico (S)", value=st.session_state.S)
with col_v1:
    st.metric(label="Variable: Intentos Fallidos", value=f"{st.session_state.intentos} / 3")
with col_v2:
    st.metric(label="Variable: Saldo", value=f"{st.session_state.saldo} Bs")

if st.session_state.S == "Bloqueado":
    st.error("🚫 TARJETA RETENIDA. Contacte a su banco para desbloquear.")
    if st.button("🔄 Simular inserción de nueva tarjeta"):
        st.session_state.S = "Autenticando"
        st.session_state.intentos = 0
        st.session_state.saldo = 5000.0
        st.session_state.logs = ["Nueva sesión iniciada."]
        st.rerun()

st.markdown("---")

# =====================================================================
# 3. FUNCIÓN DE FACTIBILIDAD Y GUARDAS (Gamma)
# =====================================================================
st.header("3. Factibilidad y Guardas Lógicas ($\Gamma$)")
st.write("$\Gamma(s, v)$ evalúa si un evento es válido dependiendo de la pantalla y el valor de las variables.")

# Factibilidad basada en la pantalla actual (S)
es_autenticando = (st.session_state.S == "Autenticando")
es_transaccion = (st.session_state.S == "Transaccion")

col_g1, col_g2 = st.columns(2)
with col_g1:
    st.write("**Factibilidad de Pantalla:**")
    st.success("✅ Permitido: Ingresar PIN" if es_autenticando else "❌ Bloqueado: Ingresar PIN")
    st.success("✅ Permitido: Solicitar Retiro" if es_transaccion else "❌ Bloqueado: Solicitar Retiro")

with col_g2:
    st.write("**Evaluación de Guardas Actuales:**")
    # Mostrar el estado matemático de las restricciones
    guarda_intentos = st.session_state.intentos < 3
    st.info(f"Condición Seguridad: [intentos < 3] -> **{guarda_intentos}**")
    st.info(f"Condición Fondos: [monto <= {st.session_state.saldo}] -> **(Evaluado al retirar)**")

st.markdown("---")

# =====================================================================
# 4. CONJUNTO DE EVENTOS PARAMETRIZADOS (E)
# =====================================================================
st.header("4. Eventos Externos ($E$)")
st.write("En la EFSM, los eventos traen 'parámetros' inyectados por el usuario (como si el PIN es válido o el monto requerido).")

def ejecutar_transicion_extendida(evento, s_nuevo, intentos_nuevos, saldo_nuevo, guarda, accion):
    s_antiguo = st.session_state.S
    v_antiguo = f"intentos={st.session_state.intentos}, saldo={st.session_state.saldo}"
    
    st.session_state.S = s_nuevo
    st.session_state.intentos = intentos_nuevos
    st.session_state.saldo = saldo_nuevo
    
    v_nuevo = f"intentos={st.session_state.intentos}, saldo={st.session_state.saldo}"
    log = f"f('{s_antiguo}', {evento}, {v_antiguo}) | Guarda: [{guarda}] -> ('{s_nuevo}', {{{v_nuevo}}}) | {accion}"
    st.session_state.logs.insert(0, log)

# Interfaz dinámica según el Estado
if es_autenticando:
    st.write("### 🔣 Evento: `Ingresar_PIN(es_valido)`")
    col_pin1, col_pin2 = st.columns(2)
    
    with col_pin1:
        if st.button("Digitar PIN CORRECTO (es_valido=True)", use_container_width=True):
            # Transición: Éxito de PIN -> Pasa a Transaccion, reinicia intentos.
            ejecutar_transicion_extendida("Ingresar_PIN(True)", "Transaccion", 0, st.session_state.saldo, "es_valido == True", "Acceso concedido.")
            st.rerun()
            
    with col_pin2:
        if st.button("Digitar PIN INCORRECTO (es_valido=False)", use_container_width=True):
            intentos_actuales = st.session_state.intentos + 1
            if intentos_actuales < 3:
                # Transición: Fallo, pero queda margen -> Se queda en Autenticando, suma intento.
                ejecutar_transicion_extendida("Ingresar_PIN(False)", "Autenticando", intentos_actuales, st.session_state.saldo, "intentos < 3", "Advertencia de PIN.")
            else:
                # Transición: Fallo crítico -> Bloqueo permanente.
                ejecutar_transicion_extendida("Ingresar_PIN(False)", "Bloqueado", intentos_actuales, st.session_state.saldo, "intentos == 3", "Límite superado. Bloqueo.")
            st.rerun()

elif es_transaccion:
    st.write("### 💵 Evento: `Solicitar_Retiro(monto)`")
    monto_solicitado = st.number_input("Ingrese monto a retirar (Bs):", min_value=10.0, step=10.0, value=100.0)
    
    if st.button("Confirmar Retiro", use_container_width=True):
        if monto_solicitado <= st.session_state.saldo:
            # Transición: Retiro Exitoso -> Resta saldo, se queda en Transaccion.
            nuevo_saldo = st.session_state.saldo - monto_solicitado
            ejecutar_transicion_extendida(f"Solicitar_Retiro({monto_solicitado})", "Transaccion", st.session_state.intentos, nuevo_saldo, f"{monto_solicitado} <= saldo", "Entrega de efectivo.")
            st.success(f"💸 Retiro exitoso de {monto_solicitado} Bs.")
        else:
            # Transición: Fondos Insuficientes -> Se queda en Transaccion, no altera variables.
            ejecutar_transicion_extendida(f"Solicitar_Retiro({monto_solicitado})", "Transaccion", st.session_state.intentos, st.session_state.saldo, f"{monto_solicitado} > saldo", "Rechazo por fondos insuficientes.")
            st.error("❌ Fondos insuficientes para esta operación.")
        st.rerun()

st.markdown("---")

# =====================================================================
# 5. FUNCIÓN DE TRANSICIÓN EXTENDIDA (f)
# =====================================================================
st.header("5. Función de Transición Extendida ($f$)")
st.write("Auditoría del cálculo de variables y evaluación de guardas:")

for log in st.session_state.logs[:8]:
    st.code(log, language="text")