import streamlit as st
import pandas as pd
import urllib.parse
import os

# 1. Configuración de pantalla Mobile First
st.set_page_config(
    page_title="Súper Chicharronazo Domicilios",
    page_icon="🥓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilos visuales tipo Rappi y tablero analítico
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #f6f7fb;
    }
    
    .stButton>button {
        width: 100%;
        height: 3rem;
        font-size: 1rem;
        font-weight: 800;
        border-radius: 12px;
        background-color: #E63946 !important;
        color: #ffffff !important;
        border: none;
        box-shadow: 0 4px 12px rgba(230, 57, 70, 0.25);
    }
    
    .rappi-card {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #eeeeee;
    }
    
    .kpi-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 16px;
        border-left: 6px solid #E63946;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        text-align: center;
    }

    .banner-nequi {
        background: linear-gradient(135deg, #20003B 0%, #3f096b 100%);
        color: #ffffff;
        border-radius: 14px;
        padding: 12px;
        text-align: center;
        margin-bottom: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Detección de Logo
LOGO_PATH = None
for nombre in ["logo.jpeg", "LOGO.jpeg", "logo.png", "LOGO.png"]:
    if os.path.exists(nombre):
        LOGO_PATH = nombre
        break

NUMERO_NEQUI_OFICIAL = "312 248 2577"

# 3. Directorio de Domiciliarios (4 en total)
REPARTIDORES = {
    1: "Xavier (Moto 1)",
    2: "Carlos (Moto 2)",
    3: "Andrés (Moto 3)",
    4: "Diego (Moto 4)"
}

# Tabla de Tarifas por Zona (Mínimo $6.000 - Máximo $12.000)
ZONAS_TARIFAS = {
    "Zona Sur Cercana (Tequendama / San Fernando)": 6000,
    "Zona Centro (San Antonio / Granada)": 8000,
    "Zona Oriente / Norte Medio (Guabal / Limonar)": 10000,
    "Zona Norte Lejana / Pance (Chipichape / Pance)": 12000
}

# Usuarios del Sistema
USUARIOS_AUTORIZADOS = {
    "cristina": {"nombre": "Cristina", "clave": "cris2026", "rol": "Administrador / Caja"},
    "xavier": {"nombre": "Xavier", "clave": "xavi2026", "rol": "Domiciliario", "rep_id": 1},
    "carlos": {"nombre": "Carlos", "clave": "car2026", "rol": "Domiciliario", "rep_id": 2},
    "andres": {"nombre": "Andrés", "clave": "and2026", "rol": "Domiciliario", "rep_id": 3},
    "diego": {"nombre": "Diego", "clave": "die2026", "rol": "Domiciliario", "rep_id": 4}
}

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.usuario_activo = None

# ==========================================
# INICIO DE SESIÓN
# ==========================================
if not st.session_state.autenticado:
    col_a, col_b, col_c = st.columns([1, 1.2, 1])
    with col_b:
        st.write("")
        if LOGO_PATH:
            st.image(LOGO_PATH, width=170)
        st.title("🥓 Súper Chicharronazo")
        st.caption("Plataforma de Operaciones y Control Financiero")
        
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

# ==========================================
# DATOS DE OPERACIÓN
# ==========================================
usuario_actual = st.session_state.usuario_activo

if "pedidos" not in st.session_state:
    st.session_state.pedidos = [
        {
            "id": 101, "cliente": "Laura Rivas", "telefono": "3154441122",
            "direccion": "Calle 9 # 44-12", "barrio": "Tequendama",
            "zona": "Zona Sur Cercana (Tequendama / San Fernando)", "flete": 6000,
            "detalle": "1x Picada Superchicharrón Personal",
            "metodo_pago": "NEQUI", "comprobante_url": "https://dummyimage.com/600x400/20003b/ffffff&text=Nequi+3122482577+Ref:+849203",
            "valor_platos": 38500, "total_cobrado": 44500, "paga_con": 0,
            "estado": "ENTREGADO", "repartidor_id": 1
        },
        {
            "id": 102, "cliente": "Andrés Mejía", "telefono": "3185559988",
            "direccion": "Carrera 56 # 13-20", "barrio": "Guabal",
            "zona": "Zona Oriente / Norte Medio (Guabal / Limonar)", "flete": 10000,
            "detalle": "1x Picada Familiar Mixta",
            "metodo_pago": "EFECTIVO", "comprobante_url": None,
            "valor_platos": 65000, "total_cobrado": 75000, "paga_con": 100000,
            "estado": "ENTREGADO", "repartidor_id": 2
        },
        {
            "id": 103, "cliente": "Felipe Gómez", "telefono": "3103332211",
            "direccion": "Avenida 6N # 28-05", "barrio": "Granada",
            "zona": "Zona Centro (San Antonio / Granada)", "flete": 8000,
            "detalle": "2x Porción Costilla Ahumada",
            "metodo_pago": "NEQUI", "comprobante_url": "https://dummyimage.com/600x400/20003b/ffffff&text=Nequi+3122482577+Ref:+110492",
            "valor_platos": 54000, "total_cobrado": 62000, "paga_con": 0,
            "estado": "ENTREGADO", "repartidor_id": 3
        },
        {
            "id": 104, "cliente": "Marcela Castro", "telefono": "3127776655",
            "direccion": "Carrera 122 # 18-40", "barrio": "Pance",
            "zona": "Zona Norte Lejana / Pance (Chipichape / Pance)", "flete": 12000,
            "detalle": "1x Picada Especial + Patacones",
            "metodo_pago": "EFECTIVO", "comprobante_url": None,
            "valor_platos": 72000, "total_cobrado": 84000, "paga_con": 100000,
            "estado": "EN_RUTA", "repartidor_id": 4
        }
    ]

# Sidebar
if LOGO_PATH:
    st.sidebar.image(LOGO_PATH, width=110)
st.sidebar.markdown(f"**{usuario_actual['nombre']}** ({usuario_actual['rol']})")

if st.sidebar.button("Cerrar Sesión"):
    st.session_state.autenticado = False
    st.session_state.usuario_activo = None
    st.rerun()

menu_opciones = ["📊 Tablero de Gestión Financiera", "🖥️ Despacho de Pedidos", "🛵 Modo Domiciliario"]
vista_seleccionada = st.sidebar.radio("Navegación:", menu_opciones)

# =========================================================
# VISTA 1: TABLERO DE GESTIÓN Y RENTABILIDAD POR ZONA
# =========================================================
if vista_seleccionada == "📊 Tablero de Gestión Financiera":
    st.title("📊 Tablero de Control y Liquidación")
    st.caption("Consolidado de ventas, distribución por zonas y pago a domiciliarios")
    
    df = pd.DataFrame(st.session_state.ped