# modulos/finanzas.py
import os
import streamlit as st
import pandas as pd
from datetime import datetime, date
from config import LINK_GOOGLE_SHEETS, REPARTIDORES

def render_finanzas():
    st.title("📊 Tablero de Control y Liquidación")
    st.caption("Consolidado de ventas de hoy, fletes y liquidación de caja con respaldo hora a hora")

    st.link_button("📂 Abrir Hoja Oficial en Google Drive", LINK_GOOGLE_SHEETS)
    st.write("")

    backups_list = sorted([f for f in os.listdir("backups") if f.endswith(".csv")], reverse=True)
    if backups_list:
        st.caption(f"🛡️ **Último respaldo automático:** `{backups_list[0]}` (Total respaldos: {len(backups_list)})")

    pedidos_reales = [p for p in st.session_state.pedidos if p.get("Estado") in ["EN_RUTA", "ENTREGADO"]]

    if not pedidos_reales:
        st.warning("Aún no hay pedidos en ruta o entregados hoy para generar el balance contable.")
    else:
        df = pd.DataFrame(pedidos_reales)
        hoy_str = date.today().strftime("%Y-%m-%d")
        ver_solo_hoy = st.checkbox("📅 Ver únicamente ventas ejecutadas hoy", value=True)
        
        if ver_solo_hoy:
            df_calc = df[df["Fecha/Hora"].astype(str).str.startswith(hoy_str)]
        else:
            df_calc = df
            
        if df_calc.empty:
            st.info("No hay ventas registradas con el filtro seleccionado.")
        else:
            df_calc["Total Cobrado ($)"] = pd.to_numeric(df_calc["Total Cobrado ($)"], errors="coerce").fillna(0)
            df_calc["Subtotal Comida ($)"] = pd.to_numeric(df_calc["Subtotal Comida ($)"], errors="coerce").fillna(0)
            df_calc["Flete ($)"] = pd.to_numeric(df_calc["Flete ($)"], errors="coerce").fillna(0)

            total_caja = df_calc["Total Cobrado ($)"].sum()
            total_comida = df_calc["Subtotal Comida ($)"].sum()
            total_fletes = df_calc["Flete ($)"].sum()
            margen = (total_comida / total_caja * 100) if total_caja > 0 else 0
            
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("💰 Total Recaudado", f"${total_caja:,.0f} COP")
            k2.metric("🥩 Venta Neta Comida", f"${total_comida:,.0f} COP")
            k3.metric("🛵 Total Fletes Repartidores", f"${total_fletes:,.0f} COP")
            k4.metric("📈 Margen Operativo Comida", f"{margen:.1f}%")
            
            csv_data = df_calc.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Base de Datos Completa (Excel / CSV)",
                data=csv_data,
                file_name=f"ventas_superchicharronazo_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
            
            st.divider()
            c_zona, c_rep = st.columns([1, 1.2])
            with c_zona:
                st.subheader("📍 Domicilios por Zona / Sector")
                res_zona = df_calc.groupby("Zona").agg(
                    Cantidad=("ID Orden", "count"),
                    Tarifa_Promedio=("Flete ($)", "mean"),
                    Total_Fletes=("Flete ($)", "sum"),
                    Venta_Comida=("Subtotal Comida ($)", "sum")
                ).reset_index()
                st.dataframe(
                    res_zona.rename(columns={
                        "Zona": "Zona / Sector",
                        "Cantidad": "Cant.",
                        "Tarifa_Promedio": "Flete Prom. ($)",
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
                    ped_r = df_calc[df_calc["Repartidor"] == r_nom]
                    carreras = len(ped_r)
                    fletes_a_pagar = ped_r["Flete ($)"].sum()
                    efectivo_en_mano = ped_r[(ped_r["Método de Pago"] == "EFECTIVO") & (ped_r["Estado"] == "ENTREGADO")]["Total Cobrado ($)"].sum()
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
                