import streamlit as st
import pandas as pd
import urllib.parse
import os

# 1. Configuración de pantalla centrada como celular (Mobile First)
st.set_page_config(
    page_title="Súper Chicharronazo Domicilios",
    page_icon="🥓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Estilos visuales tipo Rappi (UI moderna, sombras, bordes curvos y paleta de la marca)
st.markdown("""
    <style>
    /* Ocultar barra superior y pie de página de Streamlit para efecto app nativa */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Contenedor principal con fondo gris claro de app móvil */
    .stApp {
        background-color: #f6f7fb;
    }
    
    /* Botones de acción estilo Rappi */
    .stButton>button {
        width: 100%;
        height: 3.2rem;
        font-size: 1rem;
        font-weight: 800;
        border-radius: 14px;
        background-color: #E63946 !important;
        color: #ffffff !important;
        border: none;
        box-shadow: 0 4px 12px rgba(230, 57, 70, 0.25);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:active {
        transform: scale(0.98);
    }
    
    /* Tarjetas de pedidos flotantes con bordes suaves */
    .rappi-card {
        background-color: #ffffff;
        border-radius: 18px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
    }
    
    /* Encabezados de tarjeta */
    .rappi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .badge-orden {
        background-color: #111111;
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    /* Alerta de cobro Efectivo tipo Rappi */
    .badge-efectivo {
        background-color: #fff8e6;
        border: 1px solid #ffeaa7;
        color: #d68100;
        padding: 12px;
        border-radius: 14px;
        margin: 10px 0;
        font-weight: bold;
    }
    
    /* Alerta de cobro Nequi */
    .badge-nequi {
        background-color: #eafaf1;
        border: 1px solid #d4efdf;
        color: #1e8449;
        padding: 12px;
        border-radius: 14px;
        margin: 10px 0;
        font-weight: bold;
    }

    /* Caja Nequi Restaurante */
    .banner-nequi {
        background: linear-gradient(135deg, #20003B 0%, #3f096b 100%);
        color: #ffffff;
        border-radius: 16px;
        padding: 14px;
        text-align: center;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(32, 0, 59, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Detección flexible del logo
LOGO_PATH = None
for nombre in ["logo.jpeg", "LOGO.jpeg", "logo.png", "LOGO.png"]:
    if os.path.exists(nombre):
        LOGO_PATH = nombre
        break

NUMERO_NEQUI_OFICIAL = "312 248 2577"

# Usuarios autorizados
USUARIOS_AUTORIZADOS = {
    "cristina": {"nombre": "Cristina", "clave": "cris2026", "rol": "Cajero / Despacho"},
    "xavier": {"nombre": "Xavier", "clave": "xavi2026", "rol": "Domiciliario"}
}

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.usuario_activo = None

# ==========================================
# 1. PANTALLA DE ACCESO (SPLASH / LOGIN MOBILE)
# ==========================================
if not st.session_state.autenticado:
    st.write("")
    if LOGO_PATH:
        st.image(LOGO_PATH, width=190)
    else:
        st.title("🥓 SÚPER CHICHARRONAZO")
        
    st.markdown("### **Bienvenido al Sistema de Entregas**")
    st.caption("Ingresa con tu cuenta para gestionar pedidos y rutas")
    
    with st.form("form_login"):
        usuario = st.text_input("Usuario", placeholder="Ej: cristina o xavier").strip().lower()
        clave = st.text_input("Contraseña", type="password", placeholder="••••••••")
        btn_entrar = st.form_submit_button("INGRESAR")
        
        if btn_entrar:
            if usuario in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS[usuario]["clave"] == clave:
                st.session_state.autenticado = True
                st.session_state.usuario_activo = USUARIOS_AUTORIZADOS[usuario]
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
    st.stop()

# ==========================================
# 2. APLICACIÓN PRINCIPAL (SESIÓN INICIADA)
# ==========================================
usuario_actual = st.session_state.usuario_activo

# Barra de navegación superior móvil
col_logo, col_user = st.columns([1, 2])
with col_logo:
    if LOGO_PATH:
        st.image(LOGO_PATH, width=65)
with col_user:
    st.markdown(f"**Hola, {usuario_actual['nombre']}** 👋")
    st.caption(f"Perfil: {usuario_actual['rol']}")

# Estado de pedidos simulado
if "pedidos" not in st.session_state:
    st.session_state.pedidos = [
        {
            "id": 101, "cliente": "Laura Rivas", "telefono": "3154441122",
            "direccion": "Calle 9 # 44-12", "barrio": "Tequendama", "notas": "Torre B Apto 501",
            "detalle": "1x Picada Superchicharrón Personal + Porción de Patacón",
            "metodo_pago": "NEQUI", "comprobante_url": "https://dummyimage.com/600x400/20003b/ffffff&text=Nequi+3122482577+Ref:+849203",
            "total": 38500, "paga_con": 0, "estado": "PENDIENTE_PAGO", "repartidor_id": None
        },
        {
            "id": 102, "cliente": "Andrés Mejía", "telefono": "3185559988",
            "direccion": "Carrera 56 # 13-20", "barrio": "Guabal", "notas": "Casa de reja negra",
            "detalle": "1x Picada Familiar Mixta (Chicharrón, Costilla, Papa Criolla)",
            "metodo_pago": "EFECTIVO", "comprobante_url": None,
            "total": 65000, "paga_con": 100000, "estado": "EN_COCINA", "repartidor_id": None
        }
    ]

repartidores = {1: "Xavier Moto 1", 2: "Carlos Moto 2"}

# Selector de rol en barra lateral (o automático si es domiciliario)
st.sidebar.markdown(f"👤 Conectado como: **{usuario_actual['nombre']}**")
if st.sidebar.button("Cerrar Sesión"):
    st.session_state.autenticado = False
    st.session_state.usuario_activo = None
    st.rerun()

rol_elegido = st.sidebar.radio("Cambiar vista:", ["🖥️ Cajero / Despacho", "🛵 Vista Domiciliario"],
                               index=0 if usuario_actual["rol"] == "Cajero / Despacho" else 1)

# ------------------------------------------
# A. VISTA CAJERO / DESPACHO (Rappi Style)
# ------------------------------------------
if rol_elegido == "🖥️ Cajero / Despacho":
    st.markdown(f"""
        <div class="banner-nequi">
            📲 <b>Nequi Oficial:</b> <span style="font-size: 1.15rem; color: #ff007f;">{NUMERO_NEQUI_OFICIAL}</span><br>
            <small style="opacity: 0.85;">Verifica número de cuenta y referencia antes de aprobar</small>
        </div>
    """, unsafe_allow_html=True)

    tab_val, tab_asig, tab_resumen = st.tabs(["Validar Nequi", "Despacho", "Pedidos"])

    with tab_val:
        pendientes = [p for p in st.session_state.pedidos if p["estado"] == "PENDIENTE_PAGO" and p["metodo_pago"] == "NEQUI"]
        if not pendientes:
            st.success("✅ Todo al día. No hay pagos pendientes.")
        else:
            for p in pendientes:
                st.markdown(f"""
                <div class="rappi-card">
                    <div class="rappi-header">
                        <span class="badge-orden">Orden #{p['id']}</span>
                        <span style="font-weight: 800; color: #E63946; font-size: 1.1rem;">${p['total']:,.0f} COP</span>
                    </div>
                    <b>Cliente:</b> {p['cliente']} (Tel: {p['telefono']})<br>
                    🍽️ <i>{p['detalle']}</i>
                </div>
                """, unsafe_allow_html=True)
                
                st.image(p["comprobante_url"], caption=f"Comprobante Nequi #{p['id']}", use_container_width=True)
                
                c_ok, c_no = st.columns(2)
                with c_ok:
                    if st.button(f"✔ Aprobar #{p['id']}", key=f"ap_{p['id']}"):
                        p["estado"] = "EN_COCINA"
                        st.rerun()
                with c_no:
                    if st.button("❌ Rechazar", key=f"rec_{p['id']}"):
                        p["estado"] = "CANCELADO"
                        st.rerun()
                st.divider()

    with tab_asig:
        por_asignar = [p for p in st.session_state.pedidos if p["estado"] == "EN_COCINA" and p["repartidor_id"] is None]
        if not por_asignar:
            st.info("No hay pedidos en espera de repartidor.")
        else:
            for p in por_asignar:
                st.markdown(f"""
                <div class="rappi-card">
                    <div class="rappi-header">
                        <span class="badge-orden">Orden #{p['id']}</span>
                        <span style="font-weight: bold; color: #2b2b2b;">{p['metodo_pago']}</span>
                    </div>
                    📍 <b>{p['direccion']}</b> ({p['barrio']})<br>
                    👤 {p['cliente']} | 🍽️ <i>{p['detalle']}</i>
                </div>
                """, unsafe_allow_html=True)
                
                rep_sel = st.selectbox(f"Asignar repartidor a orden #{p['id']}:", 
                                      options=list(repartidores.keys()), 
                                      format_func=lambda x: repartidores[x], 
                                      key=f"r_{p['id']}")
                
                if st.button(f"🛵 Asignar a {repartidores[rep_sel]}", key=f"as_{p['id']}"):
                    p["repartidor_id"] = rep_sel
                    p["estado"] = "EN_RUTA"
                    st.rerun()
                st.divider()

    with tab_resumen:
        df = pd.DataFrame(st.session_state.pedidos)[["id", "cliente", "direccion", "metodo_pago", "total", "estado", "repartidor_id"]]
        df["repartidor"] = df["repartidor_id"].map(repartidores).fillna("Sin Asignar")
        st.dataframe(df.drop(columns=["repartidor_id"]), use_container_width=True)

# ------------------------------------------
# B. VISTA REPARTIDOR (Experiencia 100% Mobile)
# ------------------------------------------
else:
    rep_default = 1 if usuario_actual["nombre"] == "Xavier" else 2
    rep_id = st.sidebar.selectbox("Repartidor:", options=list(repartidores.keys()), 
                                  format_func=lambda x: repartidores[x], index=rep_default-1)
    
    mis_pedidos = [p for p in st.session_state.pedidos if p["repartidor_id"] == rep_id and p["estado"] != "ENTREGADO"]
    mis_entregados = [p for p in st.session_state.pedidos if p["repartidor_id"] == rep_id and p["estado"] == "ENTREGADO"]
    total_efectivo = sum(p["total"] for p in mis_entregados if p["metodo_pago"] == "EFECTIVO")
    
    st.metric(label="💵 Efectivo en mano a liquidar", value=f"${total_efectivo:,.0f} COP")
    st.write("")

    if not mis_pedidos:
        st.success("🎉 ¡Excelente! No tienes entregas pendientes.")
    else:
        for p in mis_pedidos:
            dir_enc = urllib.parse.quote(f"{p['direccion']}, {p['barrio']}, Cali")
            
            st.markdown(f"""
            <div class="rappi-card">
                <div class="rappi-header">
                    <span class="badge-orden">ENTREGA #{p['id']}</span>
                    <span style="font-weight: 800; color: #111;">${p['total']:,.0f} COP</span>
                </div>
                <h4 style="margin: 4px 0;">{p['cliente']}</h4>
                📍 <b>{p['direccion']}</b> ({p['barrio']})<br>
                📝 <i>Ref: {p['notas']}</i><br>
                🥡 <i>Llevar: {p['detalle']}</i>
            </div>
            """, unsafe_allow_html=True)
            
            if p["metodo_pago"] == "EFECTIVO":
                vuelto = p["paga_con"] - p["total"] if p["paga_con"] > p["total"] else 0
                st.markdown(f"""
                <div class="badge-efectivo">
                    💵 <b>COBRAR EN EFECTIVO:</b> ${p['total']:,.0f} COP<br>
                    El cliente paga con: ${p['paga_con']:,.0f}<br>
                    👉 <b>Dar vuelto: ${vuelto:,.0f} COP</b>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="badge-nequi">
                    ✅ <b>PAGADO POR NEQUI</b> (No cobrar nada)
                </div>
                """, unsafe_allow_html=True)
            
            # Botones de acción directos
            c1, c2, c3 = st.columns(3)
            with c1: st.link_button("🚗 Waze", f"https://waze.com/ul?q={dir_enc}&navigate=yes")
            with c2: st.link_button("🗺️ Maps", f"https://www.google.com/maps/search/?api=1&query={dir_enc}")
            with c3: st.link_button("📞 Llamar", f"tel:{p['telefono']}")
            
            st.write("")
            if st.button(f"🏁 Marcar Entregado #{p['id']}", key=f"ent_{p['id']}"):
                p["estado"] = "ENTREGADO"
                st.rerun()
            st.divider()