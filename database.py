# database.py
import os
import shutil
import pandas as pd
import streamlit as st
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

CSV_FILE = "pedidos.csv"
BACKUP_DIR = "backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

COLUMNAS_BD = [
    "ID Orden", "Fecha/Hora", "Fecha Pactada", "Hora Pactada", "Tipo Pedido", 
    "Cliente", "Teléfono", "Dirección", "Barrio", "Zona", "Platos Solicitados", 
    "Subtotal Comida ($)", "Flete ($)", "Total Cobrado ($)", "Método de Pago", "Repartidor", "Estado"
]

def respaldar_hora_a_hora():
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        stamp_hora = datetime.now().strftime("%Y%m%d_%H00")
        backup_path = os.path.join(BACKUP_DIR, f"pedidos_backup_{stamp_hora}.csv")
        shutil.copyfile(CSV_FILE, backup_path)

def cargar_pedidos():
    """Lee siempre desde Google Sheets como fuente principal permanente."""
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_cloud = conn.read(ttl=0)
        if df_cloud is not None and not df_cloud.empty:
            for c in COLUMNAS_BD:
                if c not in df_cloud.columns:
                    df_cloud[c] = ""
            df_limpio = df_cloud[COLUMNAS_BD].dropna(how="all")
            registros = df_limpio.to_dict(orient="records")
            df_limpio.to_csv(CSV_FILE, index=False)
            return registros
    except Exception:
        pass

    # Respaldo local si no hay internet momentáneamente
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            for c in COLUMNAS_BD:
                if c not in df.columns:
                    df[c] = ""
            return df[COLUMNAS_BD].to_dict(orient="records")
        except Exception:
            pass

    return []

def guardar_pedidos(lista_pedidos):
    """Guarda localmente y sincroniza de inmediato en Google Sheets permanente."""
    if lista_pedidos:
        df = pd.DataFrame(lista_pedidos)
        for col in COLUMNAS_BD:
            if col not in df.columns:
                df[col] = ""
        df = df[COLUMNAS_BD]
        df.to_csv(CSV_FILE, index=False)
        respaldar_hora_a_hora()

        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            conn.update(data=df)
        except Exception as e:
            st.error(f"⚠️ Error al escribir en Google Sheets: Asegúrate de que la hoja tenga permisos de Editor públicos.")
    else:
        df_vacio = pd.DataFrame(columns=COLUMNAS_BD)
        df_vacio.to_csv(CSV_FILE, index=False)