import streamlit as st
import pandas as pd
import urllib.parse
import os

# 1. Configuración de pantalla
st.set_page_config(
    page_title="Súper Chicharronazo - Domicilios",
    page_icon="🥓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilos visuales Rappi-Style
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #f7f8fa;
        color: #111111;
    }
    
    .stButton>button {
        width: 100%;
        height: 3rem;
        font-size: 1rem;
        font-weight: 800;
        border-radius: 12px;
        background-color: #D90429 !important;
        color: #ffffff !important;
        border: none;
        box-shadow: 0 4px 12px rgba(217, 4, 41, 0.25);
    }
    
    .rappi-card {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid #ededed;
    }
    
    .badge-orden {
        background-color: #111111;
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 14px;
        font-size: 0.85rem;
        font-weight: bold;
    }

    .banner-nequi {
        background: linear-gradient(135deg, #20003B 0%, #3f096b 100%);
        color: #ffffff;
        border-radius: 14px;
        padding: 14px;
        text-align: center;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(32, 0, 59, 0.2);
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

# 3. Catálogo de Productos (Modifica los valores cuando tengas los precios definitivos)
MENU_PRODUCTOS = {
    "Picada Superchicharrón Personal": 35000,
    "Picada Mixta Mediana (2 personas)": 60000,
    "Picada Familiar Súper Chicharronazo (4 personas)": 115000,
    "Costilla Ahumada al Barril (Porción 400g)": 38000,
    "Chicharrón Crispy Tradicional (Porción 350g)": 28000,
    "Porción de Patacones con Hogao": 12000,
    "Porción de Papa Criolla Frita": 10000,
    "Gaseosa Personal 400ml": 5000,
    "Cerveza Club Colombia / Corona": 8000
}

# 4. Tabla de Fletes por Zona (Mínimo $6.000 - Máximo $12.000)
ZONAS_TARIFAS = {
    "Zona Sur Cercana (Tequendama / San Fernando / Tejares)": 6000,
    "Zona Centro (San Antonio / Granada / Versalles)": 8000,
    "Zona Oriente y Norte Medio (Guabal / Limonar / Flora)": 10000,
    "Zona Norte Lejana y Pance (Chipichape / Menga / Pance / Cd. Jardín)": 12000
}

# 5. Los 4 Domiciliarios
REPARTIDORES = {
    1: "Xavier (Moto 1)",
    2: "Carlos (Moto 2)",
    3: "Andrés (Moto 3)",
    4: "Diego (Moto 4)"
}

# 6. Usuarios del Sistema
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
# LOGIN SCREEN
# ==========================================
if not st.session_state.autenticado:
    col_izq, col_form, col_der = st.columns([1, 1.2, 1])
    with col_form:
        st.write("")
        if LOGO_PATH:
            st.image(LOGO_PATH, width=190)
        st.title("🥓 SÚPER CHICHARRONAZO")
        st.caption("Control de Domicilios, Zonas y Liquidación de Caja")
        
        with st.form("form_login"):
            usuario = st.text_input("Usuario:").strip().lower()
            clave = st.text_input("Contraseña:", type="password")
            if st.form_submit_button("INGRESAR"):
                if usuario in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS[usuario]["clave"] == clave:
                    st.session_state.autenticado = True
                    st.session_state.usuario_activo = USUARIOS_AUTORIZADOS[usuario]
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
    st.stop()

# ==========================================
# APLICACIÓN AUTENTICADA
# ==========================================
usuario_actual = st.session_state.usuario_activo

# Base de datos en memoria para pedidos
if "pedidos" not in st.session_state:
    st.session_state.pedidos = []

# Barra lateral
if LOGO_PATH:
    st.sidebar.image(LOGO_PATH, width=120)
st.sidebar.markdown(f"👤 **{usuario_actual['nombre']}**")
st.sidebar.caption(f"Perfil: {usuario_actual['rol']}")

if st.sidebar.button("Cerrar Sesión"):
    st.session_state.autenticado = False
    st.session_state.usuario_activo = None
    st.rerun()

menu_opciones = ["🖥️ Despacho de Pedidos", "📊 Tablero de Gestión Financiera", "🛵 Modo Domiciliario"]
vista_seleccionada = st.sidebar.radio("Ir a:", menu_opciones)

# =========================================================
# VISTA 1: DESPACHO (REGISTRO ASISTIDO Y AUTOMÁTICO)
# =========================================================
if vista_seleccionada == "🖥️ Despacho de Pedidos":
    st.title("🖥️ Despacho y Registro de Pedidos")
    
    st.markdown(f"""
        <div class="banner-nequi">
            📲 <b>Nequi Oficial Restaurante:</b> <span style="font-size: 1.2rem; color: #ff007f;">{NUMERO_NEQUI_OFICIAL}</span>
            <br><small style="opacity: 0.9;">Verifica que todo comprobante recibido por WhatsApp coincida con este número.</small>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("➕ Tomar Nuevo Pedido de WhatsApp", expanded=True):
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            cliente_nom = st.text_input("Nombre del Cliente:", placeholder="Ej: Camila Ortiz")
            cliente_tel = st.text_input("Teléfono WhatsApp:", placeholder="Ej: 3112345678")
            cliente_dir = st.text_input("Dirección de Entrega:", placeholder="Ej: Cra 66 # 10-45")
            cliente_barrio = st.text_input("Barrio:", placeholder="Ej: Limonar")
        
        with col_c2:
            zona_elegida = st.selectbox("Zona de Entrega:", list(ZONAS_TARIFAS.keys()))
            costo_flete = ZONAS_TARIFAS[zona_elegida]
            st.info(f"🛵 Tarifa de domicilio para esta zona: **${costo_flete:,.0f} COP** (calculada automáticamente)")
            
            domiciliario_asig = st.selectbox(
                "Asignar Repartidor:", 
                list(REPARTIDORES.keys()), 
                format_func=lambda x: REPARTIDORES[x]
            )

        st.markdown("#### 🍽️ Selección de Platos de la Carta")
        platos_seleccionados = st.multiselect(
            "Selecciona los productos solicitados por el cliente:",
            options=list(MENU_PRODUCTOS.keys())
        )
        
        # Cálculo automático de platos
        subtotal_comida = sum(MENU_PRODUCTOS[item] for item in platos_seleccionados)
        total_a_cobrar = subtotal_comida + costo_flete
        
        st.markdown(f"""
        <div style="background-color: #fff3cd; padding: 12px; border-radius: 10px; border-left: 5px solid #ffb703; margin: 10px 0;">
            💵 <b>Subtotal Comida:</b> ${subtotal_comida:,.0f} COP | 
            🛵 <b>Domicilio:</b> ${costo_flete:,.0f} COP | 
            <span style="font-size: 1.15rem; color: #D90429;"><b>TOTAL A COBRAR: ${total_a_cobrar:,.0f} COP</b></span>
        </div>
        """, unsafe_allow_html=True)
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            metodo_pago = st.selectbox("Método de Pago:", ["NEQUI", "EFECTIVO"])
        with col_p2:
            paga_con = 0
            if metodo_pago == "EFECTIVO":
                paga_con = st.number_input("¿Con cuánto billete paga el cliente?", min_value=float(total_a_cobrar), step=10000.0, value=float(total_a_cobrar))
                vueltos_calc = paga_con - total_a_cobrar
                st.caption(f"👉 **Vueltos que el repartidor debe llevar:** ${vueltos_calc:,.0f} COP")

        if st.button("🚀 Enviar Pedido a Cocina y Domiciliario"):
            if not cliente_nom or not cliente_dir or not platos_seleccionados:
                st.error("Por favor completa el nombre, dirección y al menos un producto.")
            else:
              nuevo_id = (max([p["id"] for p in st.session_state.pedidos]) + 1) if st.session_state.pedidos else 101
                st.session_state.pedidos.append({
                    "id": nuevo_id,
                    "cliente": cliente_nom,
                    "telefono": cliente_tel,
                    "direccion": cliente_dir,
                    "barrio": cliente_barrio,
                    "zona": zona_elegida,
                    "flete": costo_flete,
                    "detalle": ", ".join(platos_seleccionados),
                    "metodo_pago": metodo_pago,
                    "subtotal_comida": subtotal_comida,
                    "total_cobrado": total_a_cobrar,
                    "paga_con": paga_con,
                    "estado": "EN_RUTA",
                    "repartidor_id": domiciliario_asig
                })
                st.success(f"✅ ¡Pedido #{nuevo_id} generado con éxito y despachado a {REPARTIDORES[domiciliario_asig]}!")
                st.rerun() 