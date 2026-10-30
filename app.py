import streamlit as st
import pandas as pd
import urllib.parse
import os
import re
from datetime import datetime, date, time

# 1. Configuración de pantalla Mobile First
st.set_page_config(
    page_title="Súper Chicharronazo - Domicilios",
    page_icon="🥓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Archivo de persistencia de datos (permanente)
CSV_FILE = "pedidos.csv"

def cargar_pedidos():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            # Asegurar compatibilidad de columnas nuevas
            if "fecha_entrega_pactada" not in df.columns:
                df["fecha_entrega_pactada"] = df["fecha"].apply(lambda x: str(x)[:10] if pd.notna(x) else "")
            if "hora_entrega_pactada" not in df.columns:
                df["hora_entrega_pactada"] = "Inmediata"
            if "tipo_pedido" not in df.columns:
                df["tipo_pedido"] = "INMEDIATO"
            return df.to_dict(orient="records")
        except Exception:
            return []
    return []

def guardar_pedidos(lista_pedidos):
    if lista_pedidos:
        df = pd.DataFrame(lista_pedidos)
        df.to_csv(CSV_FILE, index=False)

def formatear_telefono_co(tel):
    if not tel:
        return ""
    limpio = re.sub(r"\D", "", str(tel))
    if len(limpio) == 10 and limpio.startswith("3"):
        return f"57{limpio}"
    elif limpio.startswith("57") and len(limpio) == 12:
        return limpio
    return limpio

def reproducir_alerta_sonora():
    st.components.v1.html("""
        <script>
        try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const now = ctx.currentTime;
            
            const osc1 = ctx.createOscillator();
            const gain1 = ctx.createGain();
            osc1.type = 'sine';
            osc1.frequency.setValueAtTime(880, now);
            gain1.gain.setValueAtTime(0.3, now);
            gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
            osc1.connect(gain1);
            gain1.connect(ctx.destination);
            osc1.start(now);
            osc1.stop(now + 0.35);

            const osc2 = ctx.createOscillator();
            const gain2 = ctx.createGain();
            osc2.type = 'sine';
            osc2.frequency.setValueAtTime(1174.66, now + 0.2);
            gain2.gain.setValueAtTime(0.4, now + 0.2);
            gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.7);
            osc2.connect(gain2);
            gain2.connect(ctx.destination);
            osc2.start(now + 0.2);
            osc2.stop(now + 0.7);
        } catch (e) {
            console.log("Audio no habilitado:", e);
        }
        </script>
    """, height=0)

# 2. Estilos visuales
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

    .card-programado {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border-left: 6px solid #3a86ff;
        border-top: 1px solid #ededed;
        border-right: 1px solid #ededed;
        border-bottom: 1px solid #ededed;
    }
    
    .alerta-nueva-orden {
        background: linear-gradient(135deg, #D90429 0%, #ef233c 100%);
        color: #ffffff;
        padding: 14px;
        border-radius: 14px;
        text-align: center;
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 16px;
        box-shadow: 0 4px 14px rgba(217, 4, 41, 0.35);
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .badge-orden {
        background-color: #111111;
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 14px;
        font-size: 0.85rem;
        font-weight: bold;
    }

    .badge-agendado {
        background-color: #3a86ff;
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

LOGO_PATH = None
for nombre in ["logo.jpeg", "LOGO.jpeg", "logo.png", "LOGO.png"]:
    if os.path.exists(nombre):
        LOGO_PATH = nombre
        break

NUMERO_NEQUI_OFICIAL = "312 248 2577"
LINK_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/1CIM4KVvcYqZz1li65hGzfxhvKGIjEzb9OVZwv5MPAQ4/edit"

# Catálogo Oficial
MENU_PRODUCTOS = {
    "Personal": 20000,
    "Mixta": 30000,
    "Mixta Sencilla": 40000,
    "Chorizo Tradicional": 10000,
    "Mixta Familiar": 50000,
    "MegaFamiliar": 80000
}

# Tarifas por Zona
ZONAS_TARIFAS = {
    "Zona Sur Cercana (Tequendama / San Fernando / Tejares)": 6000,
    "Zona Centro (San Antonio / Granada / Versalles)": 8000,
    "Zona Oriente y Norte Medio (Guabal / Limonar / Flora)": 10000,
    "Zona Norte Lejana y Pance (Chipichape / Menga / Pance / Cd. Jardín)": 12000
}

# Domiciliarios
REPARTIDORES = {
    1: "Xavier (Moto 1)",
    2: "Carlos (Moto 2)",
    3: "Andrés (Moto 3)",
    4: "Diego (Moto 4)"
}

USUARIOS_AUTORIZADOS = {
    "cristina": {"nombre": "Cristina", "clave": "cris2026", "rol": "ADMIN", "rep_id": None},
    "xavier": {"nombre": "Xavier", "clave": "xavi2026", "rol": "DOMICILIARIO", "rep_id": 1},
    "carlos": {"nombre": "Carlos", "clave": "car2026", "rol": "DOMICILIARIO", "rep_id": 2},
    "andres": {"nombre": "Andrés", "clave": "and2026", "rol": "DOMICILIARIO", "rep_id": 3},
    "diego": {"nombre": "Diego", "clave": "die2026", "rol": "DOMICILIARIO", "rep_id": 4}
}

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.usuario_activo = None

if "pedidos" not in st.session_state:
    st.session_state.pedidos = cargar_pedidos()

# =========================================================
# LOGIN
# =========================================================
if not st.session_state.autenticado:
    col_izq, col_form, col_der = st.columns([1, 1.2, 1])
    with col_form:
        st.write("")
        if LOGO_PATH:
            st.image(LOGO_PATH, width=180)
        st.title("🥓 SÚPER CHICHARRONAZO")
        st.caption("Acceso Seguro por Rol Operativo")
        
        with st.form("form_login"):
            usuario = st.text_input("Usuario (ej. cristina o xavier):").strip().lower()
            clave = st.text_input("Contraseña:", type="password")
            if st.form_submit_button("INGRESAR"):
                if usuario in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS[usuario]["clave"] == clave:
                    st.session_state.autenticado = True
                    st.session_state.usuario_activo = USUARIOS_AUTORIZADOS[usuario]
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas.")
    st.stop()

# =========================================================
# USUARIO ACTIVO
# =========================================================
usuario_actual = st.session_state.usuario_activo

if LOGO_PATH:
    st.sidebar.image(LOGO_PATH, width=110)
st.sidebar.markdown(f"👤 **{usuario_actual['nombre']}**")
rol_etiqueta = "Administradora / Caja" if usuario_actual["rol"] == "ADMIN" else f"Repartidor ({REPARTIDORES.get(usuario_actual['rep_id'])})"
st.sidebar.caption(f"Rol: {rol_etiqueta}")

if st.sidebar.button("Cerrar Sesión"):
    st.session_state.autenticado = False
    st.session_state.usuario_activo = None
    st.rerun()

# =========================================================
# MÓDULO DOMICILIARIOS
# =========================================================
if usuario_actual["rol"] == "DOMICILIARIO":
    rep_id = usuario_actual["rep_id"]
    rep_nombre = REPARTIDORES[rep_id]
    
    st.title(f"🛵 Entregas: {rep_nombre}")
    st.caption("Gestiona tus carreras activas y cobros en tiempo real")
    
    # Solo pedidos en ruta (no agendados a futuro)
    mis_pedidos = [p for p in st.session_state.pedidos if p.get("repartidor_id") == rep_id and p.get("estado") == "EN_RUTA"]
    mis_completados = [p for p in st.session_state.pedidos if p.get("repartidor_id") == rep_id and p.get("estado") == "ENTREGADO"]
    
    clave_conteo = f"conteo_pendientes_{rep_id}"
    conteo_actual = len(mis_pedidos)
    conteo_previo = st.session_state.get(clave_conteo, conteo_actual)
    
    if conteo_actual > conteo_previo:
        reproducir_alerta_sonora()
        st.markdown("""
            <div class="alerta-nueva-orden">
                🔔 ¡NUEVA ORDEN ASIGNADA! Revisa los detalles abajo para despachar.
            </div>
        """, unsafe_allow_html=True)
        st.toast("🔔 ¡Tienes un nuevo pedido asignado!", icon="🛵")
    
    st.session_state[clave_conteo] = conteo_actual

    ganancia_fletes = sum(p.get("flete", 0) for p in mis_completados)
    
    c_met1, c_met2 = st.columns(2)
    c_met1.metric("💵 Mis Fletes Ganados", f"${ganancia_fletes:,.0f} COP")
    c_met2.metric("📦 Pedidos Pendientes", f"{len(mis_pedidos)}")
    
    if st.button("🔄 Actualizar Mis Entregas"):
        st.session_state.pedidos = cargar_pedidos()
        st.rerun()
    
    st.write("")
    
    if not mis_pedidos:
        st.success("🎉 ¡Excelente trabajo! No tienes entregas en ruta en este momento.")
    else:
        for p in mis_pedidos:
            dir_url = urllib.parse.quote(f"{p['direccion']}, {p['barrio']}, Cali")
            st.markdown(f"""
            <div class="rappi-card">
                <span class="badge-orden">ENTREGA #{p['id']}</span>
                <span style="float: right; font-weight: bold; color: #111; font-size: 1.15rem;">${p['total_cobrado']:,.0f} COP</span>
                <h3 style="margin: 6px 0;">{p['cliente']}</h3>
                📍 <b>Dirección:</b> {p['direccion']} ({p['barrio']})<br>
                🥡 <b>Llevar:</b> {p['detalle']}<br>
                🛵 <b>Tu Pago por Carrera:</b> <span style="color: #2b9348; font-weight: bold;">${p['flete']:,.0f} COP</span>
            </div>
            """, unsafe_allow_html=True)
            
            if p["metodo_pago"] == "EFECTIVO":
                vueltos = p["paga_con"] - p["total_cobrado"] if p["paga_con"] > p["total_cobrado"] else 0
                st.warning(f"💵 COBRAR EN EFECTIVO: ${p['total_cobrado']:,.0f} COP (Paga con: ${p['paga_con']:,.0f} | Cambio: ${vueltos:,.0f} COP)")
            else:
                st.success("✅ PAGADO POR NEQUI (No cobrar dinero)")
                
            c1, c2, c3 = st.columns(3)
            with c1: st.link_button("🚗 Waze", f"https://waze.com/ul?q={dir_url}&navigate=yes")
            with c2: st.link_button("🗺️ Maps", f"https://www.google.com/maps/search/?api=1&query={dir_url}")
            with c3: st.link_button("📞 Llamar", f"tel:{p['telefono']}")
            
            st.write("")
            if st.button(f"🏁 Marcar Entregado #{p['id']}", key=f"btn_ent_{p['id']}"):
                p["estado"] = "ENTREGADO"
                guardar_pedidos(st.session_state.pedidos)
                st.rerun()
            st.divider()

# =========================================================
# MÓDULO ADMINISTRADOR (CRISTINA)
# =========================================================
elif usuario_actual["rol"] == "ADMIN":
    vista_admin = st.sidebar.radio(
        "Módulo Administrativo:",
        ["🖥️ Despacho de Pedidos", "📅 Pedidos Programados / Preventas", "📊 Tablero Financiero y Caja"]
    )
    
    # -----------------------------------------------------
    # SUBVISTA 1: DESPACHO NORMAL (HOY)
    # -----------------------------------------------------
    if vista_admin == "🖥️ Despacho de Pedidos":
        st.title("🖥️ Despacho de Pedidos Inmediatos")
        
        st.markdown(f"""
            <div class="banner-nequi">
                📲 <b>Nequi Oficial Restaurante:</b> <span style="font-size: 1.2rem; color: #ff007f;">{NUMERO_NEQUI_OFICIAL}</span>
            </div>
        """, unsafe_allow_html=True)

        with st.expander("➕ Tomar Nuevo Pedido Inmediato", expanded=True):
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                cliente_nom = st.text_input("Nombre del Cliente:", placeholder="Ej: Camila Ortiz")
                cliente_tel = st.text_input("Teléfono WhatsApp:", placeholder="Ej: 3112345678")
                cliente_dir = st.text_input("Dirección de Entrega:", placeholder="Ej: Cra 66 # 10-45")
                cliente_barrio = st.text_input("Barrio:", placeholder="Ej: Limonar")
            
            with col_c2:
                zona_elegida = st.selectbox("Zona de Entrega:", list(ZONAS_TARIFAS.keys()))
                costo_flete = ZONAS_TARIFAS[zona_elegida]
                st.info(f"🛵 Domicilio automático: **${costo_flete:,.0f} COP**")
                
                domiciliario_asig = st.selectbox(
                    "Asignar Repartidor:", 
                    list(REPARTIDORES.keys()), 
                    format_func=lambda x: REPARTIDORES[x]
                )

            st.markdown("#### 🍽️ Selección de Platos")
            platos_seleccionados = st.multiselect("Productos solicitados:", options=list(MENU_PRODUCTOS.keys()))
            
            subtotal_comida = sum(MENU_PRODUCTOS[item] for item in platos_seleccionados)
            total_a_cobrar = subtotal_comida + costo_flete
            
            st.markdown(f"""
            <div style="background-color: #fff3cd; padding: 12px; border-radius: 10px; border-left: 5px solid #ffb703; margin: 10px 0;">
                💵 <b>Subtotal:</b> ${subtotal_comida:,.0f} COP | 🛵 <b>Flete:</b> ${costo_flete:,.0f} COP | 
                <span style="font-size: 1.15rem; color: #D90429;"><b>TOTAL: ${total_a_cobrar:,.0f} COP</b></span>
            </div>
            """, unsafe_allow_html=True)
            
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                metodo_pago = st.selectbox("Método de Pago:", ["NEQUI", "EFECTIVO"])
            with col_p2:
                paga_con = 0.0
                if metodo_pago == "EFECTIVO":
                    base_min = float(total_a_cobrar) if total_a_cobrar > 0 else 0.0
                    paga_con = st.number_input("¿Con cuánto paga el cliente?", min_value=base_min, step=5000.0, value=base_min)
                    vueltos_calc = paga_con - total_a_cobrar
                    st.caption(f"👉 **Vueltos para el repartidor:** ${vueltos_calc:,.0f} COP")

            if st.button("🚀 Enviar Pedido a Cocina y Domiciliario"):
                if not cliente_nom or not cliente_dir or not platos_seleccionados:
                    st.error("Por favor completa los campos principales.")
                else:
                    nuevo_id = (max([p["id"] for p in st.session_state.pedidos]) + 1) if st.session_state.pedidos else 101
                    ahora = datetime.now()
                    nuevo_pedido = {
                        "id": nuevo_id,
                        "fecha": ahora.strftime("%Y-%m-%d %H:%M"),
                        "fecha_entrega_pactada": ahora.strftime("%Y-%m-%d"),
                        "hora_entrega_pactada": "Inmediata",
                        "tipo_pedido": "INMEDIATO",
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
                    }
                    st.session_state.pedidos.append(nuevo_pedido)
                    guardar_pedidos(st.session_state.pedidos)
                    st.success(f"✅ ¡Pedido #{nuevo_id} enviado a {REPARTIDORES[domiciliario_asig]}!")
                    st.rerun()

        st.subheader("📋 Pedidos del Turno (Activos y Entregados)")
        pedidos_activos = [p for p in st.session_state.pedidos if p.get("tipo_pedido") == "INMEDIATO" or p.get("estado") in ["EN_RUTA", "ENTREGADO"]]
        if not pedidos_activos:
            st.info("No hay pedidos registrados en curso.")
        else:
            for p in reversed(pedidos_activos):
                nombre_rep = REPARTIDORES.get(p.get('repartidor_id'), 'Sin Asignar')
                msg_whatsapp = (
                    f"🥓 *¡Hola {p['cliente']}! Tu pedido de El Súper Chicharronazo ya va en camino.*\n\n"
                    f"📋 *Orden #{p['id']}*\n"
                    f"🍽️ *Detalle:* {p['detalle']}\n"
                    f"💰 *Subtotal Comida:* ${p['subtotal_comida']:,.0f} COP\n"
                    f"🛵 *Domicilio:* ${p['flete']:,.0f} COP\n"
                    f"💵 *Total a Cancelar:* ${p['total_cobrado']:,.0f} COP ({p['metodo_pago']})\n"
                    f"🛵 *Tu Domiciliario:* {nombre_rep}\n\n"
                    f"📍 *Dirección de Entrega:* {p['direccion']} ({p['barrio']})\n"
                    f"¡Gracias por tu preferencia! En breve estará en tu puerta."
                )
                tel_formateado = formatear_telefono_co(p.get("telefono", ""))
                url_whatsapp = f"https://wa.me/{tel_formateado}?text={urllib.parse.quote(msg_whatsapp)}" if tel_formateado else None

                st.markdown(f"""
                <div class="rappi-card">
                    <span class="badge-orden">Orden #{p['id']} - {p['estado']}</span>
                    <span style="float: right; font-weight: bold; color: #D90429; font-size: 1.1rem;">${p['total_cobrado']:,.0f} COP</span>
                    <h4 style="margin: 6px 0;">{p['cliente']} (Tel: {p['telefono']})</h4>
                    📍 <b>{p['direccion']}</b> ({p['barrio']}) - <i>{p['zona']}</i><br>
                    🍽️ <b>Items:</b> {p['detalle']}<br>
                    💰 <b>Comida:</b> ${p['subtotal_comida']:,.0f} | 🛵 <b>Flete:</b> ${p['flete']:,.0f} | 💳 <b>Pago:</b> {p['metodo_pago']}<br>
                    🛵 <b>Repartidor:</b> {nombre_rep}
                </div>
                """, unsafe_allow_html=True)
                
                if url_whatsapp:
                    st.link_button(f"💬 Notificar por WhatsApp a {p['cliente']} (#{p['id']})", url_whatsapp)
                st.write("")

    # -----------------------------------------------------
    # SUBVISTA 2: NUEVO MÓDULO DE PEDIDOS PROGRAMADOS
    # -----------------------------------------------------
    elif vista_admin == "📅 Pedidos Programados / Preventas":
        st.title("📅 Pedidos Programados y Preventas")
        st.caption("Agenda pedidos solicitados con anticipación y pásalos a ruta cuando corresponda.")
        
        with st.expander("➕ Agendar Nuevo Pedido para Otra Fecha", expanded=True):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                fecha_pactada = st.date_input("Fecha de entrega pactada:", min_value=date.today())
                hora_pactada = st.time_input("Hora aproximada de entrega:", value=time(13, 0))
                cli_prog_nom = st.text_input("Nombre del Cliente:", key="p_nom", placeholder="Ej: Andrés Restrepo")
                cli_prog_tel = st.text_input("Teléfono WhatsApp:", key="p_tel", placeholder="Ej: 3158889900")
            
            with col_f2:
                cli_prog_dir = st.text_input("Dirección de Entrega:", key="p_dir", placeholder="Ej: Calle 14 # 85-20")
                cli_prog_barrio = st.text_input("Barrio:", key="p_barrio", placeholder="Ej: Ciudad Jardín")
                zona_prog = st.selectbox("Zona de Entrega:", list(ZONAS_TARIFAS.keys()), key="p_zona")
                costo_flete_prog = ZONAS_TARIFAS[zona_prog]
                st.info(f"🛵 Tarifa calculada: **${costo_flete_prog:,.0f} COP**")

            st.markdown("#### 🍽️ Platos Encargados")
            platos_prog = st.multiselect("Selecciona los platos encargados:", options=list(MENU_PRODUCTOS.keys()), key="p_platos")
            subtotal_prog = sum(MENU_PRODUCTOS[item] for item in platos_prog)
            total_prog = subtotal_prog + costo_flete_prog
            
            st.markdown(f"""
            <div style="background-color: #e8f0fe; padding: 12px; border-radius: 10px; border-left: 5px solid #3a86ff; margin: 10px 0;">
                📅 <b>Fecha Pactada:</b> {fecha_pactada.strftime('%d/%m/%Y')} a las {hora_pactada.strftime('%I:%M %p')}<br>
                💵 <b>Subtotal Comida:</b> ${subtotal_prog:,.0f} COP | 🛵 <b>Flete:</b> ${costo_flete_prog:,.0f} COP | 
                <span style="font-size: 1.15rem; color: #1d3557;"><b>TOTAL: ${total_prog:,.0f} COP</b></span>
            </div>
            """, unsafe_allow_html=True)
            
            col_met1, col_met2 = st.columns(2)
            with col_met1:
                met_pago_prog = st.selectbox("Forma de Pago Acordada:", ["NEQUI", "EFECTIVO"], key="p_met")
            with col_met2:
                paga_con_prog = 0.0
                if met_pago_prog == "EFECTIVO":
                    base_m = float(total_prog) if total_prog > 0 else 0.0
                    paga_con_prog = st.number_input("Paga con billete de:", min_value=base_m, step=5000.0, value=base_m, key="p_billete")

            if st.button("📌 Guardar Pedido en Agenda"):
                if not cli_prog_nom or not cli_prog_dir or not platos_prog:
                    st.error("Completa cliente, dirección y platos para agendar.")
                else:
                    nuevo_id = (max([p["id"] for p in st.session_state.pedidos]) + 1) if st.session_state.pedidos else 101
                    pedido_agendado = {
                        "id": nuevo_id,
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "fecha_entrega_pactada": str(fecha_pactada),
                        "hora_entrega_pactada": hora_pactada.strftime("%I:%M %p"),
                        "tipo_pedido": "PROGRAMADO",
                        "cliente": cli_prog_nom,
                        "telefono": cli_prog_tel,
                        "direccion": cli_prog_dir,
                        "barrio": cli_prog_barrio,
                        "zona": zona_prog,
                        "flete": costo_flete_prog,
                        "detalle": ", ".join(platos_prog),
                        "metodo_pago": met_pago_prog,
                        "subtotal_comida": subtotal_prog,
                        "total_cobrado": total_prog,
                        "paga_con": paga_con_prog,
                        "estado": "AGENDADO",
                        "repartidor_id": None
                    }
                    st.session_state.pedidos.append(pedido_agendado)
                    guardar_pedidos(st.session_state.pedidos)
                    st.success(f"🎉 ¡Pedido #{nuevo_id} agendado exitosamente para el {fecha_pactada}!")
                    st.rerun()

        # Seguimiento de agenda
        st.divider()
        st.subheader("📋 Agenda de Pedidos por Entregar")
        
        pedidos_agendados = [p for p in st.session_state.pedidos if p.get("estado") == "AGENDADO"]
        
        if not pedidos_agendados:
            st.info("No hay pedidos agendados pendientes para fechas futuras.")
        else:
            filtro_agenda = st.radio("Filtrar agenda por:", ["Todos los agendados", "Solo los de Hoy", "A partir de Mañana"], horizontal=True)
            hoy_str = date.today().strftime("%Y-%m-%d")
            
            for p in pedidos_agendados:
                f_pactada = str(p.get("fecha_entrega_pactada", ""))
                if filtro_agenda == "Solo los de Hoy" and f_pactada != hoy_str:
                    continue
                if filtro_agenda == "A partir de Mañana" and f_pactada <= hoy_str:
                    continue
                
                st.markdown(f"""
                <div class="card-programado">
                    <span class="badge-agendado">📅 PARA: {p.get('fecha_entrega_pactada')} a las {p.get('hora_entrega_pactada')}</span>
                    <span style="float: right; font-weight: bold; color: #1d3557; font-size: 1.15rem;">${p['total_cobrado']:,.0f} COP</span>
                    <h3 style="margin: 8px 0 4px 0;">{p['cliente']} (Tel: {p['telefono']})</h3>
                    📍 <b>{p['direccion']}</b> ({p['barrio']}) - <i>{p['zona']}</i><br>
                    🍽️ <b>Menú Encargado:</b> {p['detalle']}<br>
                    💰 <b>Comida:</b> ${p['subtotal_comida']:,.0f} | 🛵 <b>Flete:</b> ${p['flete']:,.0f} | 💳 <b>Pago:</b> {p['metodo_pago']}<br>
                    📌 <b>Estado actual:</b> {p['estado']}
                </div>
                """, unsafe_allow_html=True)
                
                # Asignar y despachar
                col_desp1, col_desp2 = st.columns([1.5, 1])
                with col_desp1:
                    rep_elegido = st.selectbox(
                        f"Asignar Repartidor para Orden #{p['id']}:", 
                        list(REPARTIDORES.keys()), 
                        format_func=lambda x: REPARTIDORES[x],
                        key=f"rep_sel_{p['id']}"
                    )
                with col_desp2:
                    st.write("")
                    if st.button(f"🚀 Despachar a Ruta #{p['id']}", key=f"btn_act_{p['id']}"):
                        p["estado"] = "EN_RUTA"
                        p["repartidor_id"] = rep_elegido
                        guardar_pedidos(st.session_state.pedidos)
                        st.success(f"¡Orden #{p['id']} despachada a {REPARTIDORES[rep_elegido]}!")
                        st.rerun()

    # -----------------------------------------------------
    # SUBVISTA 3: TABLERO FINANCIERO
    # -----------------------------------------------------
    else:
        st.title("📊 Tablero de Control y Liquidación")
        st.caption("Consolidado en tiempo real de ventas, pagos a repartidores y márgenes")

        st.link_button("📂 Abrir Hoja en Google Drive", LINK_GOOGLE_SHEETS)
        st.write("")

        # Consideramos únicamente los pedidos que están en ruta o entregados para el balance contable real
        pedidos_reales = [p for p in st.session_state.pedidos if p.get("estado") in ["EN_RUTA", "ENTREGADO"]]

        if not pedidos_reales:
            st.warning("Aún no hay pedidos en ruta o entregados para balance contable.")
        else:
            df = pd.DataFrame(pedidos_reales)
            
            hoy_str = date.today().strftime("%Y-%m-%d")
            ver_solo_hoy = st.checkbox("📅 Ver únicamente ventas ejecutadas hoy", value=True)
            
            if ver_solo_hoy:
                df_calc = df[df["fecha"].astype(str).str.startswith(hoy_str)]
            else:
                df_calc = df
                
            if df_calc.empty:
                st.info("No hay ventas registradas con el filtro seleccionado.")
            else:
                total_caja = df_calc["total_cobrado"].sum()
                total_comida = df_calc["subtotal_comida"].sum()
                total_fletes = df_calc["flete"].sum()
                margen = (total_comida / total_caja * 100) if total_caja > 0 else 0
                
                k1, k2, k3, k4 = st.columns(4)
                k1.metric("💰 Total Recaudado", f"${total_caja:,.0f} COP")
                k2.metric("🥩 Venta Neta Comida", f"${total_comida:,.0f} COP")
                k3.metric("🛵 Total Fletes", f"${total_fletes:,.0f} COP")
                k4.metric("📈 Margen Comida", f"{margen:.1f}%")
                
                csv_data = df_calc.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Descargar Base de Datos Completa (Excel / CSV)",
                    data=csv_data,
                    file_name=f"pedidos_superchicharronazo_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
                
                st.divider()
                
                c_zona, c_rep = st.columns([1, 1.2])
                
                with c_zona:
                    st.subheader("📍 Domicilios por Zona")
                    res_zona = df_calc.groupby("zona").agg(
                        Cantidad=("id", "count"),
                        Tarifa=("flete", "first"),
                        Total_Fletes=("flete", "sum"),
                        Venta_Comida=("subtotal_comida", "sum")
                    ).reset_index()
                    
                    st.dataframe(
                        res_zona.rename(columns={
                            "zona": "Zona",
                            "Cantidad": "Cant.",
                            "Tarifa": "Flete ($)",
                            "Total_Fletes": "Total Domicilios ($)",
                            "Venta_Comida": "Venta Neta ($)"
                        }),
                        use_container_width=True,
                        hide_index=True
                    )

                with c_rep:
                    st.subheader("💵 Liquidación a Repartidores")
                    liq_data = []
                    for r_id, r_nom in REPARTIDORES.items():
                        ped_r = df_calc[df_calc["repartidor_id"] == r_id]
                        carreras = len(ped_r)
                        fletes_a_pagar = ped_r["flete"].sum()
                        efectivo_en_mano = ped_r[(ped_r["metodo_pago"] == "EFECTIVO") & (ped_r["estado"] == "ENTREGADO")]["total_cobrado"].sum()
                        debe_entregar_a_caja = efectivo_en_mano - fletes_a_pagar
                        
                        liq_data.append({
                            "Repartidor": r_nom,
                            "Viajes": carreras,
                            "Pago Fletes": fletes_a_pagar,
                            "Efectivo Recaudado": efectivo_en_mano,
                            "Cuadre a Caja": debe_entregar_a_caja
                        })
                        
                    df_liq = pd.DataFrame(liq_data)
                    st.dataframe(
                        df_liq.style.format({
                            "Pago Fletes": "${:,.0f}",
                            "Efectivo Recaudado": "${:,.0f}",
                            "Cuadre a Caja": "${:,.0f}"
                        }),
                        use_container_width=True,
                        hide_index=True
                    )