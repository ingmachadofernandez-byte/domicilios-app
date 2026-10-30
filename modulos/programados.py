# modulos/programados.py
import streamlit as st
import urllib.parse
from datetime import datetime, date, time
from config import MENU_PRODUCTOS, REPARTIDORES, CELULAR_ENCARGADA_DESPACHOS
from database import guardar_pedidos
from modulos.utils import formatear_telefono_co, reproducir_alerta_sonora

@st.dialog("🔔 ¡NUEVO PEDIDO AGENDADO CON ÉXITO!")
def mostrar_popup_agenda(pedido):
    reproducir_alerta_sonora()
    st.markdown(f"""
    <div style="background-color: #e8f0fe; padding: 14px; border-radius: 12px; border-left: 5px solid #1E88E5; margin-bottom: 12px;">
        <h4 style="margin: 0; color: #1565C0;">📋 Reserva #{pedido.get('ID Orden')}</h4>
        <p style="margin: 6px 0 0 0; color: #111;">
            📅 <b>Fecha y Hora:</b> {pedido.get('Fecha Pactada')} a las {pedido.get('Hora Pactada')}<br>
            👤 <b>Cliente:</b> {pedido.get('Cliente')} ({pedido.get('Teléfono')})<br>
            📍 <b>Dirección:</b> {pedido.get('Dirección')} ({pedido.get('Barrio')})<br>
            🥩 <b>Menú:</b> {pedido.get('Platos Solicitados')}<br>
            💰 <b>Total:</b> ${float(pedido.get('Total Cobrado ($)', 0)):,.0f} COP ({pedido.get('Método de Pago')})
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mensaje formateado para la encargada de despachos
    msg_despachos = (
        f"🚨 *¡ALERTA NUEVA PREVENTA AGENDADA!* 🚨\n\n"
        f"📋 *Reserva #{pedido.get('ID Orden')}*\n"
        f"📅 *Entrega Pactada:* {pedido.get('Fecha Pactada')} a las {pedido.get('Hora Pactada')}\n"
        f"👤 *Cliente:* {pedido.get('Cliente')}\n"
        f"📞 *Teléfono Cliente:* {pedido.get('Teléfono')}\n"
        f"📍 *Dirección:* {pedido.get('Dirección')} ({pedido.get('Barrio')})\n"
        f"🍽️ *Menú Solicitado:* {pedido.get('Platos Solicitados')}\n"
        f"💵 *Total a Cancelar:* ${float(pedido.get('Total Cobrado ($)', 0)):,.0f} COP ({pedido.get('Método de Pago')})\n\n"
        f"⚠️ *Por favor tener presente para alistamiento en cocina y ruta.*"
    )
    
    tel_encargada = formatear_telefono_co(CELULAR_ENCARGADA_DESPACHOS)
    url_wa_encargada = f"https://wa.me/{tel_encargada}?text={urllib.parse.quote(msg_despachos)}"
    
    st.link_button("📲 Notificar por WhatsApp a Despachos (311 758 5987)", url_wa_encargada)
    
    # También enlace para confirmar al cliente
    tel_cliente = formatear_telefono_co(pedido.get("Teléfono", ""))
    if tel_cliente:
        msg_cliente = (
            f"🥓 *¡Hola {pedido.get('Cliente')}! Confirmamos tu pedido programado en El Súper Chicharronazo.*\n\n"
            f"📋 *Reserva #{pedido.get('ID Orden')}*\n"
            f"📅 *Fecha de Entrega:* {pedido.get('Fecha Pactada')} a las {pedido.get('Hora Pactada')}\n"
            f"🍽️ *Menú Encargado:* {pedido.get('Platos Solicitados')}\n"
            f"💰 *Subtotal Comida:* ${float(pedido.get('Subtotal Comida ($)', 0)):,.0f} COP\n"
            f"🛵 *Domicilio:* ${float(pedido.get('Flete ($)', 0)):,.0f} COP\n"
            f"💵 *Total Acordado:* ${float(pedido.get('Total Cobrado ($)', 0)):,.0f} COP ({pedido.get('Método de Pago')})\n\n"
            f"📍 *Dirección de Entrega:* {pedido.get('Dirección')} ({pedido.get('Barrio')})\n"
            f"¡Tu orden ya está registrada en nuestro sistema!"
        )
        url_wa_cliente = f"https://wa.me/{tel_cliente}?text={urllib.parse.quote(msg_cliente)}"
        st.link_button(f"💬 Enviar Confirmación al Cliente ({pedido.get('Cliente')})", url_wa_cliente)

    if st.button("Cerrar Aviso"):
        st.session_state.ultimo_agendado_popup = None
        st.rerun()

def render_programados():
    st.title("📅 Pedidos Programados y Preventas")
    st.caption("Agenda pedidos anticipados con alerta sonora, popup de confirmación y aviso automático a despachos.")

    # Disparar popup si se acaba de agendar un pedido
    f"🚨 *¡ALERTA NUEVA PREVENTA AGENDADA!* 🚨\n\n"
    f"📋 *Reserva #{pedido.get('ID Orden')}*\n"
    f"📅 *Entrega Pactada:* {pedido.get('Fecha Pactada')} a las {pedido.get('Hora Pactada')}\n"
    f"👤 *Cliente:* {pedido.get('Cliente')}\n"
    f"📞 *Teléfono Cliente:* {pedido.get('Teléfono')}\n"
    f"📍 *Dirección:* {pedido.get('Dirección')} ({pedido.get('Barrio')})\n"
    f"🍽️ *Menú Solicitado:* {pedido.get('Platos Solicitados')}\n"
    f"💵 *Total a Cancelar:* ${float(pedido.get('Total Cobrado ($)', 0)):,.0f} COP ({pedido.get('Método de Pago')})\n\n"
    f"⚠️ *Por favor tener presente para alistamiento en cocina y ruta.*"
)

st.markdown("##### 📲 Notificar a Encargadas de Despacho:")
col_enc1, col_enc2 = st.columns(2)

tel_1 = formatear_telefono_co(ENCARGADAS_DESPACHO["Encargada 1"])
url_wa_1 = f"https://wa.me/{tel_1}?text={urllib.parse.quote(msg_despachos)}"
with col_enc1:
    st.link_button("📲 Avisar al 311 758 5487", url_wa_1)

tel_2 = formatear_telefono_co(ENCARGADAS_DESPACHO["Encargada 2"])
url_wa_2 = f"https://wa.me/{tel_2}?text={urllib.parse.quote(msg_despachos)}"
with col_enc2:
    st.link_button("📲 Avisar al 300 379 0386", url_wa_2)
        
        with col_f2:
            cli_prog_dir = st.text_input("Dirección de Entrega:", key="p_dir", placeholder="Ej: Calle 14 # 85-20")
            cli_prog_barrio = st.text_input("Barrio:", key="p_barrio", placeholder="Ej: Ciudad Jardín")
            costo_flete_prog = st.number_input("Valor del Domicilio ($):", min_value=0, max_value=20000, value=6000, step=1000, key="p_flete_manual")
            zona_prog = st.text_input("Zona / Sector:", key="p_zona_manual", placeholder="Ej: Pance / Tequendama")

        st.markdown("#### 🍽️ Selección de Platos y Cantidades para Reserva")
        cantidades_prog = {}
        cols_prog = st.columns(3)
        idx_p = 0
        for plato, precio in MENU_PRODUCTOS.items():
            with cols_prog[idx_p % 3]:
                cant_p = st.number_input(f"**{plato}** (${precio:,.0f})", min_value=0, max_value=30, value=0, step=1, key=f"prog_cant_{plato}")
                if cant_p > 0:
                    cantidades_prog[plato] = cant_p
            idx_p += 1

        subtotal_prog = sum(MENU_PRODUCTOS[plato] * cant for plato, cant in cantidades_prog.items())
        total_prog = subtotal_prog + costo_flete_prog
        detalle_prog_str = ", ".join([f"{cant}x {plato}" for plato, cant in cantidades_prog.items()]) if cantidades_prog else ""

        st.markdown(f"""
        <div style="background-color: #e8f0fe; padding: 12px; border-radius: 10px; border-left: 5px solid #3a86ff; margin: 10px 0;">
            📅 <b>Fecha Pactada:</b> {fecha_pactada.strftime('%d/%m/%Y')} a las {hora_pactada.strftime('%I:%M %p')}<br>
            🥩 <b>Platos Encargados:</b> {detalle_prog_str if detalle_prog_str else 'Ninguno'}<br>
            💵 <b>Subtotal Comida:</b> ${subtotal_prog:,.0f} COP | 🛵 <b>Flete:</b> ${costo_flete_prog:,.0f} COP | 
            <span style="font-size: 1.15rem; color: #1d3557;"><b>TOTAL A COBRAR: ${total_prog:,.0f} COP</b></span>
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

        if st.button("📌 Guardar Pedido en Agenda y Disparar Alerta"):
            if not cli_prog_nom or not cli_prog_dir or not cantidades_prog:
                st.error("Completa cliente, dirección y selecciona al menos 1 plato para agendar.")
            else:
                pedidos = st.session_state.pedidos
                # Para pedidos agendados, el consecutivo corresponde a la fecha en que se entregará
                f_pactada_str = str(fecha_pactada)
                pedidos_fecha_pactada = [p for p in pedidos if str(p.get("Fecha Pactada", "")) == f_pactada_str]
                consecutivo_dia = len(pedidos_fecha_pactada) + 1
                nuevo_id = f"{consecutivo_dia:02d}"  # Formato: 01, 02, 03...
                pedido_agendado = {
                    "ID Orden": nuevo_id,
                    "Fecha/Hora": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Fecha Pactada": str(fecha_pactada),
                    "Hora Pactada": hora_pactada.strftime("%I:%M %p"),
                    "Tipo Pedido": "PROGRAMADO",
                    "Cliente": cli_prog_nom,
                    "Teléfono": cli_prog_tel,
                    "Dirección": cli_prog_dir,
                    "Barrio": cli_prog_barrio,
                    "Zona": zona_prog if zona_prog else "Cali General",
                    "Platos Solicitados": detalle_prog_str,
                    "Subtotal Comida ($)": subtotal_prog,
                    "Flete ($)": costo_flete_prog,
                    "Total Cobrado ($)": total_prog,
                    "Método de Pago": met_pago_prog,
                    "Repartidor": "Sin Asignar",
                    "Estado": "AGENDADO"
                }
                st.session_state.pedidos.append(pedido_agendado)
                guardar_pedidos(st.session_state.pedidos)
                
                # Activar popup emergente y sonido
                st.session_state.ultimo_agendado_popup = pedido_agendado
                st.rerun()

    st.divider()
    st.subheader("📋 Agenda de Pedidos por Entregar")
    pedidos_agendados = [p for p in st.session_state.pedidos if p.get("Estado") == "AGENDADO"]
    
    if not pedidos_agendados:
        st.info("No hay pedidos agendados pendientes para fechas futuras.")
    else:
        filtro_agenda = st.radio("Filtrar agenda por:", ["Todos los agendados", "Solo los de Hoy", "A partir de Mañana"], horizontal=True)
        hoy_str = date.today().strftime("%Y-%m-%d")
        
        for p in pedidos_agendados:
            f_pactada = str(p.get("Fecha Pactada", ""))
            if filtro_agenda == "Solo los de Hoy" and f_pactada != hoy_str:
                continue
            if filtro_agenda == "A partir de Mañana" and f_pactada <= hoy_str:
                continue
            
            # Notificación para encargada de despachos
            msg_alerta_despachos = (
                f"🚨 *RECORDATORIO DE PREVENTA PENDIENTE* 🚨\n\n"
                f"📋 *Reserva #{p.get('ID Orden')}*\n"
                f"📅 *Entrega:* {p.get('Fecha Pactada')} a las {p.get('Hora Pactada')}\n"
                f"👤 *Cliente:* {p.get('Cliente')} ({p.get('Teléfono')})\n"
                f"📍 *Dirección:* {p.get('Dirección')} ({p.get('Barrio')})\n"
                f"🍽️ *Menú:* {p.get('Platos Solicitados')}\n"
                f"💵 *Total:* ${float(p.get('Total Cobrado ($)', 0)):,.0f} COP ({p.get('Método de Pago')})"
            )
            tel_enc = formatear_telefono_co(CELULAR_ENCARGADA_DESPACHOS)
            url_wa_enc = f"https://wa.me/{tel_enc}?text={urllib.parse.quote(msg_alerta_despachos)}"

            st.markdown(f"""
            <div class="card-programado">
                <span class="badge-agendado">📅 RESERVA: {p.get('Fecha Pactada')} ({p.get('Hora Pactada')})</span>
                <span style="float: right; font-weight: bold; color: #1d3557; font-size: 1.15rem;">${float(p.get('Total Cobrado ($)', 0)):,.0f} COP</span>
                <h3 style="margin: 8px 0 4px 0;">{p.get('Cliente')} (Tel: {p.get('Teléfono')})</h3>
                📍 <b>{p.get('Dirección')}</b> ({p.get('Barrio')}) - <i>{p.get('Zona', 'Cali')}</i><br>
                🍽️ <b>Menú:</b> {p.get('Platos Solicitados')}<br>
                💰 <b>Comida:</b> ${float(p.get('Subtotal Comida ($)', 0)):,.0f} | 🛵 <b>Flete:</b> ${float(p.get('Flete ($)', 0)):,.0f} | 💳 <b>Pago:</b> {p.get('Método de Pago')}<br>
                📌 <b>Estado:</b> {p.get('Estado')}
            </div>
            """, unsafe_allow_html=True)

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                st.link_button(f"🚨 Avisar a Despachos (311 758 5987)", url_wa_enc)
            with col_btn2:
                tel_c = formatear_telefono_co(p.get("Teléfono", ""))
                if tel_c:
                    msg_cli = (
                        f"🥓 *¡Hola {p.get('Cliente')}! Recordamos tu reserva en El Súper Chicharronazo.*\n"
                        f"📋 Orden #{p.get('ID Orden')} para el {p.get('Fecha Pactada')} ({p.get('Hora Pactada')}).\n"
                        f"En breve pasaremos tu orden a cocina y ruta."
                    )
                    url_c = f"https://wa.me/{tel_c}?text={urllib.parse.quote(msg_cli)}"
                    st.link_button(f"💬 Notificar al Cliente", url_c)
            
            # Despachar a ruta cuando llegue la hora
            col_desp1, col_desp2 = st.columns([1.5, 1])
            with col_desp1:
                rep_elegido = st.selectbox(
                    f"Asignar Repartidor para Orden #{p.get('ID Orden')}:", 
                    list(REPARTIDORES.keys()), 
                    format_func=lambda x: REPARTIDORES[x],
                    key=f"rep_sel_{p.get('ID Orden')}"
                )
            with col_desp2:
                st.write("")
                if st.button(f"🚀 Despachar a Ruta #{p.get('ID Orden')}", key=f"btn_act_{p.get('ID Orden')}"):
                    p["Estado"] = "EN_RUTA"
                    p["Repartidor"] = REPARTIDORES[rep_elegido]
                    guardar_pedidos(st.session_state.pedidos)
                    st.success(f"¡Orden #{p.get('ID Orden')} despachada a {REPARTIDORES[rep_elegido]}!")
                    st.rerun()
            st.divider()