import os, shutil, sqlite3, re
from datetime import datetime
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform
from kivy.metrics import dp

def get_base_dir():
    if platform == 'android':
        try:
            from android.storage import app_storage_path
            return app_storage_path()
        except:
            return MDApp.get_running_app().user_data_dir
    else:
        return os.path.dirname(os.path.abspath(__file__))

def get_paths():
    BASE = get_base_dir()
    DB_DIR = os.path.join(BASE, "BASE_DE_DATOS")
    RESP_DIR = os.path.join(BASE, "RESPALDOS")
    GEN_DIR = os.path.join(BASE, "ARCHIVOS_GENERADOS")
    os.makedirs(DB_DIR, exist_ok=True)
    os.makedirs(RESP_DIR, exist_ok=True)
    os.makedirs(GEN_DIR, exist_ok=True)
    return DB_DIR, RESP_DIR, GEN_DIR

def init_db():
    DB_DIR, _, _ = get_paths()
    con=sqlite3.connect(os.path.join(DB_DIR,"datos.db"))
    con.execute("""CREATE TABLE IF NOT EXISTS registros(
        id INTEGER PRIMARY KEY,
        tipo TEXT,
        contenido TEXT,
        categoria TEXT,
        fecha TEXT)""")
    con.commit(); con.close()

def add_registro(tipo, contenido, categoria):
    DB_DIR, _, _ = get_paths()
    con=sqlite3.connect(os.path.join(DB_DIR,"datos.db"))
    fecha=datetime.now().strftime("%Y-%m-%d %H:%M")
    con.execute("INSERT INTO registros(tipo,contenido,categoria,fecha) VALUES (?,?,?,?)",
                (tipo, contenido, categoria, fecha))
    con.commit(); con.close()

def get_registros():
    DB_DIR, _, _ = get_paths()
    con=sqlite3.connect(os.path.join(DB_DIR,"datos.db"))
    cur=con.cursor()
    cur.execute("SELECT tipo,contenido,categoria,fecha FROM registros ORDER BY id DESC")
    data=cur.fetchall(); con.close()
    return data

def get_ram_info():
    ram_gb = 0
    try:
        if os.path.exists("/proc/meminfo"):
            with open("/proc/meminfo") as f:
                for line in f:
                    if "MemTotal" in line:
                        kb = int(re.findall(r'\d+', line)[0])
                        ram_gb = kb / 1024 / 1024
                        break
        else:
            ram_gb = 4.0
    except:
        ram_gb = 4.0

    if ram_gb < 2.5:
        sugerencia = "qwen2.5:0.5b (512MB) - Tu equipo tiene poca RAM"
    elif ram_gb < 4.5:
        sugerencia = "qwen2.5:1.5b (1GB) - Ideal para tu equipo"
    elif ram_gb < 7:
        sugerencia = "qwen2.5-coder:3b (2GB) - Recomendado"
    else:
        sugerencia = "qwen2.5:7b / deepseek-coder-v2:7b (4GB+) - Tu equipo aguanta"

    return f"{ram_gb:.1f} GB detectados", sugerencia

def ia_categorizar(texto):
    texto = texto.lower()
    if any(x in texto for x in ["cliente", "pagar", "cobrar", "venta", "dinero"]):
        return "FINANZAS"
    if any(x in texto for x in ["comprar", "tienda", "super", "mercado"]):
        return "COMPRAS"
    if any(x in texto for x in ["llamar", "cita", "reunion", "cliente", "telefono"]):
        return "CONTACTOS"
    if any(x in texto for x in ["urgente", "hoy", "importante"]):
        return "URGENTE"
    return "GENERAL"

def hacer_respaldo():
    DB_DIR, RESP_DIR, _ = get_paths()
    o=os.path.join(DB_DIR,"datos.db")
    if os.path.exists(o):
        d=os.path.join(RESP_DIR,f"respaldo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
        shutil.copy(o,d); return d

def generar_informe():
    _, _, GEN_DIR = get_paths()
    regs=get_registros()
    ram, modelo = get_ram_info()
    txt=f"INFORME OFFGRID GestorMasterS - {datetime
