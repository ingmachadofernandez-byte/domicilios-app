# database.py
import os
import shutil
import json
import requests
import pandas as pd
import streamlit as st
from datetime import datetime
from config import LINK_GOOGLE_SHEETS, URL_WEBHOOK_SHEETS

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
    # 1. Leer directamente desde el CSV export público de Google Sheets (fuente permanente)
    try:
        sheet_id = LINK_GOOGLE_SHEETS.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
        df_cloud = pd.read_csv(csv_url)
        if df_cloud is not None and not df_cloud.empty:
            for c in COLUMNAS_BD:
                if c not in df_cloud.columns:
                    df_cloud[c] = ""
            df_limpio = df_cloud[COLUMNAS_BD].dropna(how="all")
            if not df_limpio.empty:
                df_limpio.to_csv(CSV_FILE, index=False)
                return df_limpio.to_dict(orient="records")
    except Exception:
        pass

    # 2. Respaldo local si la conexión falla momentáneamente
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
    if lista_pedidos:
        df = pd.DataFrame(lista_pedidos)
        for col in COLUMNAS_BD:
            if col not in df.columns:
                df[col] = ""
        df = df[COLUMNAS_BD]
        df.to_csv(CSV_FILE, index=False)
        respaldar_hora_a_hora()

        # Enviar inmediatamente por el Webhook de Google Apps Script con redirecciones habilitadas
        if URL_WEBHOOK_SHEETS and "http" in URL_WEBHOOK_SHEETS:
            try:
                filas_para_sheet = df.fillna("").astype(str).values.tolist()
                payload = {
                    "action": "sync_all",
                    "rows": filas_para_sheet
                }
                requests.post(
                    URL_WEBHOOK_SHEETS, 
                    data=json.dumps(payload), 
                    headers={"Content-Type": "application/json"}, 
                    timeout=15,
                    allow_redirects=True
                )
            except Exception as e:
                pass
    else:
        df_vacio = pd.DataFrame(columns=COLUMNAS_BD)
        df_vacio.to_csv(CSV_FILE, index=False)