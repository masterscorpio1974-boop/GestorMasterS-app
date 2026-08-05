import os, shutil, sqlite3, re
from datetime import datetime
# ── NUEVOS IMPORTS YA AGREGADOS ──
from kivymd.app import MDApp
from kivy.utils import platform
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

# ==================== TUS RUTAS ORIGINALES ====================
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

# ==================== BASE DE DATOS ====================
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
    con.execute("INSERT INTO registros(tipo,contenido,categoria,fecha) VALUES (?,?,?,?)",tipo, contenido,categoria, fecha)
    con.commit(); con.close()

def get_registros():
    DB_DIR, _, _ = get_paths()
    con=sqlite3.connect(os.path.join(DB_DIR,"datos.db"))
    cur=con.cursor()
    cur.execute("SELECT tipo,contenido,categoria,fecha FROM registros ORDER BY id DESC")
    data=cur.fetchall(); con.close()
    return data

# ==================== LECTURA DE MEMORIA ARREGLADA ====================
def get_ram_info():
    ram_gb = 0.0
    try:
        # Primero por sistema Android nativo
        if platform == 'android':
            from jnius import autoclass
            ActivityManager = autoclass('android.app.ActivityManager')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            am = PythonActivity.mActivity.getSystemService(ActivityManager.ACTIVITY_SERVICE)
            memInfo = ActivityManager.MemoryInfo()
            am.getMemoryInfo(memInfo)
            ram_gb = round(memInfo.totalMem / (1024**3), 1)
        else:
            # Si corre en PC
            import psutil
            ram_gb = round(psutil.virtual_memory().total / (1024**3), 1)
    except:
        # Respaldo con tu metodo original
        try:
            if os.path.exists("/proc/meminfo"):
                with open("/proc/meminfo") as f:
                    for line in f:
                        if "MemTotal" in line:
                            kb = int(re.findall(r'\d+', line)[0])
                            ram_gb = round(kb / 1024 / 1024, 1)
                            break
        except:
            ram_gb = 4.0

    # TU MISMA LOGICA DE RECOMENDACIONES
    if ram_gb < 2.5:
        sugerencia = "qwen2.5:0.5b (512MB) - Tu equipo tiene poca RAM"
    elif ram_gb < 4.5:
        sugerencia = "qwen2.5:1.5b (1GB) - Ideal para tu equipo"
    elif ram_gb < 7:
        sugerencia = "qwen2.5:3b (2GB) - Recomendado"
    else:
        sugerencia = "qwen2.5:7b / deepseek-coder-v2:7b (4GB+) - Tu equipo aguanta"

    return f"{ram_gb:.1f} GB detectados", sugerencia

# ==================== CATEGORIZACION ====================
def ia_categorizar(texto):
    texto = texto.lower()
    if any(x in texto for x in ["cliente", "pagar", "cobrar", "venta", "dinero"]):
        return "FINANZAS"
    if any(x in texto for x in ["comprar", "tienda", "super", "mercado"]):
        return "COMPRAS"
    if any(x in texto for x in ["llamar", "cita", "reunion", "cliente", "telefono"]):
        return "CONTACTOS"
    if any(x in texto for x in ["hoy", "importante"]):
        return "URGENTE"
    return "GENERAL"

# ==================== RESPALDOS ====================
def hacer_respaldo():
    DB_DIR, RESP_DIR, _ = get_paths()
    if os.path.exists(os.path.join(DB_DIR,"datos.db")):
        d=os.path.join(RESP_DIR,f"respaldo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
        shutil.copy(os.path.join(DB_DIR,"datos.db"),d); return d

def generar_informe():
    _, _, GEN_DIR = get_paths()
    regs=get_registros()
    ram, modelo = get_ram_info()
    txt=f"INFORME GestorMasterS - {datetime.now().strftime('%d/%m/%Y %H:%M')}\n{ram}\nModelo recomendado: {modelo}\n---\n"
    for r in regs: txt += f"{r[3]} | {r[0]} | {r[2]}\n{r[1]}\n---\n"
    arch=os.path.join(GEN_DIR,f"informe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(arch,"w",encoding="utf-8")as f: f.write(txt)
    return arch

# ==================== INICIO DE APP ====================
if __name__ == "__main__":
    init_db()
    # Aqui se agregara tu interfaz completa cuando quieras
    print("GestorMasterS iniciado correctamente")
    print(get_ram_info())
