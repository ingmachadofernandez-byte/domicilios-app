# modulos/domiciliarios.py
import streamlit as st
import urllib.parse
from config import REPARTIDORES
from database import cargar_pedidos, guardar_pedidos
from modulos.utils import reproducir_alerta_sonora

def render_domiciliario(usuario_actual):
    rep_id = usuario_actual["rep_id"]
    rep_nombre = REPARTIDORES[rep_id]
    
    st.title(f"🛵 Entregas: {rep_nombre}")
    st.caption("Gestiona tus carreras activas y cobros en tiempo real")
    
    mis_pedidos = [p for p in st.session_state.pedidos if p.get("Repartidor") == rep_nombre and p.get("Estado") == "EN_RUTA"]
    mis_completados = [p for p in st.session_state.pedidos if p.get("Repartidor") == rep_nombre and p.get("Estado") == "ENTREGADO"]
    
    clave_conteo = f"conteo_pendientes_{rep_id}"
    conteo_actual = len(mis_pedidos)
    conteo_previo = st.session_state.get(clave_conteo, conteo_actual)
    
    if conteo_actual > conteo_previo:
        reproducir_alerta_sonora()
        st.toast("🔔 ¡Tienes un nuevo pedido asignado!", icon="🛵")
    
    st.session_state[clave_conteo] = conteo_actual

    ganancia_fletes = sum(float(p.get("Flete ($)", 0)) for p in mis_completados)
    
    c_met1, c_met2 = st.columns(2)
    c_met1.metric("💵 Mis Fletes Ganados Hoy", f"${ganancia_fletes:,.0f} COP")
    c_met2.metric("📦 Pedidos Pendientes", f"{len(mis_pedidos)}")
    
    if st.button("🔄 Actualizar Mis Entregas"):
        st.session_state.pedidos = cargar_pedidos()
        st.rerun()
    
    st.write("")
    
    if not mis_pedidos:
        st.success("🎉 ¡Excelente trabajo! No tienes entregas en ruta en este momento.")
    else:
        for p in mis_pedidos:
            dir_url = urllib.parse.quote(f"{p.get('Dirección')}, {p.get('Barrio')}, Cali")
            total_cobrado = float(p.get("Total Cobrado ($)", 0))
            flete = float(p.get("Flete ($)", 0))
            
            st.markdown(f"""
            <div class="rappi-card">
                <span class="badge-orden">ENTREGA #{p.get('ID Orden')}</span>
                <span style="float: right; font-weight: bold; color: #111; font-size: 1.15rem;">${total_cobrado:,.0f} COP</span>
                <h3 style="margin: 6px 0;">{p.get('Cliente')}</h3>
                📍 <b>Dirección:</b> {p.get('Dirección')} ({p.get('Barrio')})<br>
                🥡 <b>Llevar:</b> {p.get('Platos Solicitados')}<br>
                🛵 <b>Tu Pago por Carrera:</b> <span style="color: #2b9348; font-weight: bold;">${flete:,.0f} COP</span>
            </div>
            """, unsafe_allow_html=True)
            
            if p.get("Método de Pago") == "EFECTIVO":
                st.warning(f"💵 COBRAR EN EFECTIVO: ${total_cobrado:,.0f} COP")
            else:
                st.success("✅ PAGADO POR NEQUI (No cobrar dinero)")
                
            c1, c2, c3 = st.columns(3)
            with c1: st.link_button("🚗 Waze", f"https://waze.com/ul?q={dir_url}&navigate=yes")
            with c2: st.link_button("🗺️ Maps", f"https://www.google.com/maps/search/?api=1&query={dir_url}")
            with c3: st.link_button("📞 Llamar", f"tel:{p.get('Teléfono')}")
            
            st.write("")
            if st.button(f"🏁 Marcar Entregado #{p.get('ID Orden')}", key=f"btn_ent_{p.get('ID Orden')}"):
                p["Estado"] = "ENTREGADO"
                guardar_pedidos(st.session_state.pedidos)
                st.rerun()
            st.divider()
            