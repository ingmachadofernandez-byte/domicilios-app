# Enviar inmediatamente por el Webhook de Google Apps Script
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