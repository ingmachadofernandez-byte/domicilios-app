# modulos/utils.py
import re
import os
import streamlit as st

def obtener_ruta_logo():
    for nombre in ["logo.jpeg", "LOGO.jpeg", "logo.png", "LOGO.png"]:
        if os.path.exists(nombre):
            return nombre
    return None

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
        } catch (e) {}
        </script>
    """, height=0)

def inyectar_estilos():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        html, body, [class*="css"], .stApp {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background-color: #F8F9FA !important;
            color: #1A1D20 !important;
        }
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        .block-container {
            padding-top: 1.2rem !important;
            padding-bottom: 3rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 900px !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            display: flex; gap: 6px; background: #ECEFF1; padding: 5px;
            border-radius: 14px; box-shadow: inset 0 1px 3px rgba(0,0,0,0.06);
        }
        .stTabs [data-baseweb="tab"] {
            flex: 1; height: 44px; background-color: transparent; border-radius: 10px;
            color: #5A626A; font-weight: 700; font-size: 0.88rem; border: none;
            text-align: center; justify-content: center; padding: 0 8px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #FFFFFF !important; color: #1A1D20 !important;
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08) !important;
        }
        .stButton>button {
            width: 100%; height: 3.2rem; font-size: 0.95rem; font-weight: 700;
            border-radius: 14px; background: linear-gradient(135deg, #B8001F 0%, #880808 100%) !important;
            color: #FFFFFF !important; border: none !important;
            box-shadow: 0 6px 18px rgba(184, 0, 31, 0.28) !important;
        }
        .rappi-card {
            background: #FFFFFF; border-radius: 18px; padding: 18px;
            margin-bottom: 16px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
            border: 1px solid #EAECEF;
        }
        .card-programado {
            background: #FFFFFF; border-radius: 18px; padding: 18px;
            margin-bottom: 16px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
            border: 1px solid #EAECEF; border-left: 6px solid #1E88E5;
        }
        .badge-orden {
            background: #1A1D20; color: #FFFFFF; padding: 4px 12px;
            border-radius: 20px; font-size: 0.78rem; font-weight: 700;
            text-transform: uppercase; display: inline-block;
        }
        .badge-agendado {
            background: #E3F2FD; color: #1565C0; padding: 4px 12px;
            border-radius: 20px; font-size: 0.78rem; font-weight: 700; display: inline-block;
        }
        .banner-nequi {
            background: linear-gradient(135deg, #1C0A35 0%, #31145A 100%);
            color: #FFFFFF; border-radius: 16px; padding: 16px; text-align: center;
            margin-bottom: 18px; box-shadow: 0 6px 20px rgba(28, 10, 53, 0.25);
        }
        </style>
    """, unsafe_allow_html=True)