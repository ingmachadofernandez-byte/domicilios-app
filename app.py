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
    else:
        columnas = ["id", "fecha", "fecha_entrega_pactada", "hora_entrega_pactada", "tipo_pedido", 
                    "cliente", "telefono", "direccion", "barrio", "zona", "flete", "detalle", 
                    "metodo_pago", "subtotal_comida", "total_cobrado", "paga_con", "estado", "repartidor_id"]
        df_vacio = pd.DataFrame(columns=columnas)
        df_vacio.to_csv(CSV_FILE, index=False)

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
            console.log("Audio no disponible:", e);
        }
        </script>
    """, height=0)

# 2. Estilos Visuales Gourmet Mobile-First
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #F8F9FA !important;
        color: #1A1D20 !important;
        -webkit-font-smoothing: antialiased;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 900px !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        gap: 6px;
        background: #ECEFF1;
        padding: 5px;
        border-radius: 14px;
        border: none;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.06);
    }
    
    .stTabs [data-baseweb="tab"] {
        flex: 1;
        height: 44px;
        background-color: transparent;
        border-radius: 10px;
        color: #5A626A;
        font-weight: 700;
        font-size: 0.88rem;
        border: none;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: center;
        justify-content: center;
        padding: 0 10px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #1A1D20 !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04) !important;
    }

    .stButton>button {
        width: 100%;
        height: 3.2rem;
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.3px;
        border-radius: 14px;
        background: linear-gradient(135deg, #B8001F 0%, #880808 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 6px 18px rgba(184, 0, 31, 0.28) !important;
        transition: all 0.2s ease;
    }

    .stButton>button:active {
        transform: scale(0.98);
        box-shadow: 0 2px 8px rgba(184, 0, 31, 0.2) !important;
    }

    .rappi-card {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
        border: 1px solid #EAECEF;
    }

    .card-programado {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
        border: 1px solid #EAECEF;
        border-left: 6px solid #1E88E5;
    }

    .badge-orden {
        background: #1A1D20;
        color: #FFFFFF;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        display: inline-block;
    }

    .badge-agendado {
        background: #E3F2FD;
        color: #1565C0;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        display: inline-block;
    }

    .banner-nequi {
        background: linear-gradient(135deg, #1C0A35 0%, #31145A 100%);
        color: #FFFFFF;
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        margin-bottom: 18px;
        box-shadow: 0 6px 20px rgba(28, 10, 53, 0.25);
    }

    .alerta-nueva-orden {
        background: linear-gradient(135deg, #B8001F 0%, #D32F2F 100%);
        color: #FFFFFF;
        padding: 16px;
        border-radius: 16px;
        text-align: center;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 16px;
        box-shadow: 0 8px 24px rgba(184, 0, 31, 0.35);
        animation: pulseSubtle 2s infinite;
    }

    @keyframes pulseSubtle {
        0% { transform: scale(1); }
        50% { transform: scale(1.015); }
        100% { transform: scale(1); }
    }

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        padding: 14px 16px;
        border-radius: 16px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
        border: 1px solid #EAECEF;
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

# Domiciliarios Oficiales
REPARTIDORES = {
    1: "Xavier (Moto 1)",
    2: "Carlos (Moto 2)",
    3: "Andrés (Moto 3)",
    4: "Diego (Moto 4)",
    5: "Gustavo (Moto 5)",
    6: "Yango (Moto 6)"
}

# Credenciales de Acceso
USUARIOS_AUTORIZADOS = {
    "cristina": {"nombre": "Cristina", "clave": "cris2026", "rol": "ADMIN", "rep_id": None},
    "catalina": {"nombre": "Catalina", "clave": "cata2026", "rol": "ADMIN", "rep_id": None},
    "xavier": {"nombre": "Xavier", "clave": "xavi2026", "rol": "DOMICILIARIO", "rep_id": 1},
    "carlos": {"nombre": "Carlos", "clave": "car2026", "rol": "DOMICILIARIO", "rep_id": 2},
    "andres": {"nombre": "Andrés", "clave": "and2026", "rol": "DOMICILI