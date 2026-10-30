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

# Encabezados exactos de tu Google Sheet
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
    # 1. Intentar cargar desde Google Sheets
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_cloud = conn.read(ttl="0s")
        if df_cloud is not None and not df_cloud.empty:
            for c in COLUMNAS_BD:
                if c not in df_cloud.columns:
                    df_cloud[c] = ""
            registros = df_cloud[COLUMNAS_BD].to_dict(orient="records")
            df_cloud[COLUMNAS_BD].to_csv(CSV_FILE, index=False)
            return registros
    except Exception:
        pass

    # 2. Respaldo local
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            for c in COLUMNAS_BD:
                if c not in df.columns:
                    df[c] = ""
            return df.to_dict(orient="records")
        except Exception:
            pass

    # 3. Intentar recuperar desde último backup
    backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith(".csv")])
    if backups:
        try:
            ultimo = os.path.join(BACKUP_DIR, backups[-1])
            df = pd.read_csv(ultimo)
            return df.to_dict(orient="records")
        except Exception:
            return []
    return []

def guardar_pedidos(lista_pedidos):
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
            st.warning(f"Guardado localmente. Sincronización en la nube pendiente: {e}")
    else:
        df_vacio = pd.DataFrame(columns=COLUMNAS_BD)
        df_vacio.to_csv(CSV_FILE, index=False)
        