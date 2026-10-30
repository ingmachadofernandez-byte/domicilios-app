# app.py
import streamlit as st
from config import USUARIOS_AUTORIZADOS, REPARTIDORES
from database import cargar_pedidos
from modulos.utils import inyectar_estilos, obtener_ruta_logo
from modulos.despacho import render_despacho
from modulos.programados import render_programados
from modulos.finanzas import render_finanzas
from modulos.domiciliarios import render_domiciliario

st.set_page_config(
    page_title="Súper Chicharronazo - Domicilios",
    page_icon="🥓",
    layout="wide",
    initial_sidebar_state="expanded"
)

inyectar_estilos()
logo_path = obtener_ruta_logo()

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.usuario_activo = None

if "pedidos" not in st.session_state:
    st.session_state.pedidos = cargar_pedidos()

# PANTALLA LOGIN
if not st.session_state.autenticado:
    _, col_form, _ = st.columns([1, 1.2, 1])
    with col_form:
        st.write("")
        if logo_path:
            st.image(logo_path, width=180)
        st.title("🥓 SÚPER CHICHARRONAZO")
        st.caption("Acceso Seguro por Rol Operativo")
        
        with st.form("form_login"):
            usuario = st.text_input("Usuario:").strip().lower()
            clave = st.text_input("Contraseña:", type="password")
            if st.form_submit_button("INGRESAR"):
                if usuario in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS[usuario]["clave"] == clave:
                    st.session_state.autenticado = True
                    st.session_state.usuario_activo = USUARIOS_AUTORIZADOS[usuario]
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas.")
    st.stop()

# SESIÓN ACTIVA
usuario_actual = st.session_state.usuario_activo

if logo_path:
    st.sidebar.image(logo_path, width=110)
st.sidebar.markdown(f"👤 **{usuario_actual['nombre']}**")
rol_txt = "Administradora / Caja" if usuario_actual["rol"] == "ADMIN" else f"Repartidor ({REPARTIDORES.get(usuario_actual['rep_id'])})"
st.sidebar.caption(f"Rol: {rol_txt}")

if st.sidebar.button("Cerrar Sesión"):
    st.session_state.autenticado = False
    st.session_state.usuario_activo = None
    st.rerun()

# ENRUTAMIENTO POR MÓDULOS
if usuario_actual["rol"] == "DOMICILIARIO":
    render_domiciliario(usuario_actual)
elif usuario_actual["rol"] == "ADMIN":
    tab_despacho, tab_programados, tab_finanzas = st.tabs([
        "🖥️ Despacho Inmediato", 
        "📅 Pedidos Programados / Preventas", 
        "📊 Tablero Financiero y Descarga Excel"
    ])
    with tab_despacho:
        render_despacho()
    with tab_programados:
        render_programados()
    with tab_finanzas:
        render_finanzas()