# modulos/despacho.py
import streamlit as st
import urllib.parse
from datetime import datetime
from config import MENU_PRODUCTOS, REPARTIDORES, NUMERO_NEQUI_OFICIAL
from database import guardar_pedidos
from modulos.utils import formatear_telefono_co

def render_despacho():
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
            cliente_tel = st.text_input("Teléfono WhatsApp (10 dígitos):", placeholder="Ej: 3112345678")
            cliente_dir = st.text_input("Dirección de Entrega:", placeholder="Ej: Cra 66 # 10-45")
            cliente_barrio = st.text_input("Barrio:", placeholder="Ej: Limonar")
        
        with col_c2:
            costo_flete = st.number_input("Valor del Domicilio ($):", min_value=0, max_value=20000, value=6000, step=1000)
            zona_elegida = st.text_input("Zona / Sector / Comuna:", placeholder="Ej: San Fernando / Comuna 17")
            domiciliario_asig = st.selectbox("Asignar Repartidor:", list(REPARTIDORES.keys()), format_func=lambda x: REPARTIDORES[x])

        st.markdown("#### 🍽️ Selección de Platos y Cantidades")
        cantidades_orden = {}
        cols_menu = st.columns(3)
        idx = 0
        for plato, precio in MENU_PRODUCTOS.items():
            with cols_menu[idx % 3]:
                cant = st.number_input(f"**{plato}** (${precio:,.0f})", min_value=0, max_value=20, value=0, step=1, key=f"inm_cant_{plato}")
                if cant > 0:
                    cantidades_orden[plato] = cant
            idx += 1
        
        subtotal_comida = sum(MENU_PRODUCTOS[plato] * cant for plato, cant in cantidades_orden.items())
        total_a_cobrar = subtotal_comida + costo_flete
        detalle_platos_str = ", ".join([f"{cant}x {plato}" for plato, cant in cantidades_orden.items()]) if cantidades_orden else ""
        
        st.markdown(f"""
        <div style="background-color: #fff3cd; padding: 14px; border-radius: 12px; border-left: 5px solid #ffb703; margin: 12px 0;">
            🥩 <b>Platos seleccionados:</b> {detalle_platos_str if detalle_platos_str else 'Ninguno'}<br>
            💵 <b>Subtotal Comida:</b> ${subtotal_comida:,.0f} COP | 🛵 <b>Flete:</b> ${costo_flete:,.0f} COP | 
            <span style="font-size: 1.15rem; color: #D90429;"><b>TOTAL A COBRAR: ${total_a_cobrar:,.0f} COP</b></span>
        </div>
        """, unsafe_allow_html=True)
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            metodo_pago = st.selectbox("Método de Pago:", ["NEQUI", "EFECTIVO", "DATAFONO"])
        with col_p2:
            paga_con = 0.0
            if metodo_pago == "EFECTIVO":
                base_min = float(total_a_cobrar) if total_a_cobrar > 0 else 0.0
                paga_con = st.number_input("¿Con cuánto paga el cliente?", min_value=base_min, step=5000.0, value=base_min)
                vueltos_calc = paga_con - total_a_cobrar
                st.caption(f"👉 **Vueltos para el repartidor:** ${vueltos_calc:,.0f} COP")

        if st.button("🚀 Enviar Pedido a Cocina y Domiciliario")
            if not cliente_nom or not cliente_dir or not cantidades_orden:
                st.error("Por favor completa el nombre, dirección y selecciona al menos 1 plato.")
            else:
                pedidos = st.session_state.pedidos
                hoy_str = datetime.now().strftime("%Y-%m-%d")
                # Contar pedidos registrados hoy
                pedidos_hoy = [p for p in pedidos if str(p.get("Fecha/Hora", "")).startswith(hoy_str)]
                consecutivo_hoy = len(pedidos_hoy) + 1
                nuevo_id = f"{consecutivo_hoy:02d}"  # Formato: 01, 02, 03...
                nuevo_pedido = {
        
                    "ID Orden": nuevo_id,
                    "Fecha/Hora": ahora.strftime("%Y-%m-%d %H:%M"),
                    "Fecha Pactada": ahora.strftime("%Y-%m-%d"),
                    "Hora Pactada": "Inmediata",
                    "Tipo Pedido": "INMEDIATO",
                    "Cliente": cliente_nom,
                    "Teléfono": cliente_tel,
                    "Dirección": cliente_dir,
                    "Barrio": cliente_barrio,
                    "Zona": zona_elegida if zona_elegida else "Cali General",
                    "Platos Solicitados": detalle_platos_str,
                    "Subtotal Comida ($)": subtotal_comida,
                    "Flete ($)": costo_flete,
                    "Total Cobrado ($)": total_a_cobrar,
                    "Método de Pago": metodo_pago,
                    "paga_con": paga_con,
                    "Repartidor": REPARTIDORES[domiciliario_asig],
                    "Estado": "EN_RUTA"
                }
                
                st.session_state.pedidos.append(nuevo_pedido)
                guardar_pedidos(st.session_state.pedidos)
                st.success(f"✅ ¡Pedido #{nuevo_id} guardado en BD y asignado a {REPARTIDORES[domiciliario_asig]}!")
                st.rerun()

    st.subheader("📋 Pedidos del Turno (Activos y Entregados)")
    pedidos_activos = [p for p in st.session_state.pedidos if p.get("Tipo Pedido") == "INMEDIATO" or p.get("Estado") in ["EN_RUTA", "ENTREGADO"]]
    if not pedidos_activos:
        st.info("No hay pedidos registrados en curso.")
    else:
        for p in reversed(pedidos_activos):
            nombre_rep = p.get("Repartidor", "Sin Asignar")
            msg_whatsapp = (
                f"🥓 *¡Hola {p.get('Cliente')}! Tu pedido de El Súper Chicharronazo ya va en camino.*\n\n"
                f"📋 *Orden #{p.get('ID Orden')}*\n"
                f"🍽️ *Detalle:* {p.get('Platos Solicitados')}\n"
                f"💰 *Subtotal Comida:* ${float(p.get('Subtotal Comida ($)', 0)):,.0f} COP\n"
                f"🛵 *Domicilio:* ${float(p.get('Flete ($)', 0)):,.0f} COP\n"
                f"💵 *Total a Cancelar:* ${float(p.get('Total Cobrado ($)', 0)):,.0f} COP ({p.get('Método de Pago')})\n"
                f"🛵 *Tu Domiciliario:* {nombre_rep}\n\n"
                f"📍 *Dirección de Entrega:* {p.get('Dirección')} ({p.get('Barrio')})\n"
                f"¡Gracias por tu preferencia! En breve estará en tu puerta."
            )
            tel_formateado = formatear_telefono_co(p.get("Teléfono", ""))
            url_whatsapp = f"https://wa.me/{tel_formateado}?text={urllib.parse.quote(msg_whatsapp)}" if tel_formateado else None

            st.markdown(f"""
            <div class="rappi-card">
                <span class="badge-orden">Orden #{p.get('ID Orden')} - {p.get('Estado')}</span>
                <span style="float: right; font-weight: bold; color: #D90429; font-size: 1.1rem;">${float(p.get('Total Cobrado ($)', 0)):,.0f} COP</span>
                <h4 style="margin: 6px 0;">{p.get('Cliente')} (Tel: {p.get('Teléfono')})</h4>
                📍 <b>{p.get('Dirección')}</b> ({p.get('Barrio')}) - <i>{p.get('Zona', 'Cali')}</i><br>
                🍽️ <b>Items:</b> {p.get('Platos Solicitados')}<br>
                💰 <b>Comida:</b> ${float(p.get('Subtotal Comida ($)', 0)):,.0f} | 🛵 <b>Flete:</b> ${float(p.get('Flete ($)', 0)):,.0f} | 💳 <b>Pago:</b> {p.get('Método de Pago')}<br>
                🛵 <b>Repartidor:</b> {nombre_rep}
            </div>
            """, unsafe_allow_html=True)
            
            if url_whatsapp:
                st.link_button(f"💬 Confirmar y Notificar WhatsApp a {p.get('Cliente')} (#{p.get('ID Orden')})", url_whatsapp)
            st.write("")
