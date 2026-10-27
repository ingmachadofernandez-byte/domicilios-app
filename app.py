if st.button("🚀 Enviar Pedido a Cocina y Domiciliario"):
            if not cliente_nom or not cliente_dir or not platos_seleccionados:
                st.error("Por favor completa el nombre, dirección y al menos un producto.")
            else:
                nuevo_id = (max([p["id"] for p in st.session_state.pedidos]) + 1) if st.session_state.pedidos else 101
                st.session_state.pedidos.append({
                    "id": nuevo_id,
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
                })
                st.success(f"✅ ¡Pedido #{nuevo_id} generado con éxito y despachado a {REPARTIDORES[domiciliario_asig]}!")
                st.rerun()