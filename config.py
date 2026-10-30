# config.py

NUMERO_NEQUI_OFICIAL = "312 248 2577"
CELULAR_ENCARGADA_DESPACHOS = "311 758 5987"
LINK_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/1CIM4KVvcYqZz1li65hGzfxhvKGIjEzb9OVZwv5MPAQ4/edit"

# Catálogo Oficial de Precios
MENU_PRODUCTOS = {
    "Personal": 20000,
    "Mixta": 30000,
    "Mixta Sencilla": 40000,
    "Chorizo Tradicional": 10000,
    "Mixta Familiar": 50000,
    "MegaFamiliar": 80000
}

# Domiciliarios Oficiales
REPARTIDORES = {
    1: "Xavier (Moto 1)",
    2: "Carlos (Moto 2)",
    3: "Andrés (Moto 3)",
    4: "Diego (Moto 4)",
    5: "Gustavo (Moto 5)",
    6: "Yango (Moto 6)"
}

# Credenciales de Acceso
USUARIOS_AUTORIZADOS = {
    "cristina": {"nombre": "Cristina", "clave": "cris2026", "rol": "ADMIN", "rep_id": None},
    "catalina": {"nombre": "Catalina", "clave": "cata2026", "rol": "ADMIN", "rep_id": None},
    "xavier": {"nombre": "Xavier", "clave": "xavi2026", "rol": "DOMICILIARIO", "rep_id": 1},
    "carlos": {"nombre": "Carlos", "clave": "car2026", "rol": "DOMICILIARIO", "rep_id": 2},
    "andres": {"nombre": "Andrés", "clave": "and2026", "rol": "DOMICILIARIO", "rep_id": 3},
    "diego": {"nombre": "Diego", "clave": "die2026", "rol": "DOMICILIARIO", "rep_id": 4},
    "gustavo": {"nombre": "Gustavo", "clave": "gus2026", "rol": "DOMICILIARIO", "rep_id": 5},
    "yango": {"nombre": "Yango", "clave": "yan2026", "rol": "DOMICILIARIO", "rep_id": 6}
}