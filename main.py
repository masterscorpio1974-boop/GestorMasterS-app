import os, shutil, sqlite3, re
from datetime import datetime
from kivymd.app import MDApp
from kivy.utils import platform
from kivy.lang import Builder
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
    con = sqlite3.connect(os.path.join(DB_DIR,"datos.db"))
    # Tabla vieja
    con.execute("""CREATE TABLE IF NOT EXISTS registros(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      tipo TEXT, contenido TEXT, categoria TEXT, fecha TEXT)""")
    # NUEVA TABLA QUE PEDISTE OFFGRID
    con.execute("""CREATE TABLE IF NOT EXISTS clientes(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nombre TEXT,
      direccion TEXT,
      phone TEXT,
      correo TEXT,
      ubicacion TEXT,
      otros TEXT,
      fecha TEXT)""")
    con.commit()
    con.close()
def add_registro(tipo, contenido, categoria):
    DB_DIR, _, _ = get_paths()
    con = sqlite3.connect(os.path.join(DB_DIR,"datos.db"))
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    con.execute("INSERT INTO registros(tipo,contenido,categoria,fecha) VALUES (?,?,?,?)",
                (tipo, contenido, categoria, fecha))
    con.commit()
    con.close()

def get_registros():
    DB_DIR, _, _ = get_paths()
    con = sqlite3.connect(os.path.join(DB_DIR,"datos.db"))
    cur = con.cursor()
    cur.execute("SELECT tipo,contenido,categoria,fecha FROM registros ORDER BY id DESC")
    data = cur.fetchall()
    con.close()
    return data

# ==================== LECTURA DE MEMORIA ARREGLADA ====================
def get_ram_info():
    ram_gb = 0.0
    try:
        if platform == 'android':
            from jnius import autoclass
            ActivityManager = autoclass('android.app.ActivityManager')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            am = PythonActivity.mActivity.getSystemService(ActivityManager.ACTIVITY_SERVICE)
            memInfo = ActivityManager.MemoryInfo()
            am.getMemoryInfo(memInfo)
            ram_gb = round(memInfo.totalMem / (1024**3), 1)
        else:
            import psutil
            ram_gb = round(psutil.virtual_memory().total / (1024**3), 1)
    except:
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

    # TU LÓGICA DE RECOMENDACIONES
    if ram_gb < 2.5:
        sugerencia = "qwen2.5:0.5b (512MB) - Tu equipo tiene poca RAM"
    elif ram_gb < 4.5:
        sugerencia = "qwen2.5:1.5b (1GB) - Ideal para tu equipo"
    elif ram_gb < 7:
        sugerencia = "qwen2.5:3b (2GB) - Recomendado"
    else:
        sugerencia = "qwen2.5:7b / deepseek-coder-v2:7b (4GB+) - Tu equipo aguanta"

    return f"{ram_gb:.1f} GB detectados", sugerencia

# ==================== CATEGORIZACIÓN ====================
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

# ==================== RESPALDOS E INFORMES ====================
def hacer_respaldo():
    DB_DIR, RESP_DIR, _ = get_paths()
    ruta_db = os.path.join(DB_DIR,"datos.db")
    if os.path.exists(ruta_db):
        nombre = f"respaldo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        ruta_nueva = os.path.join(RESP_DIR, nombre)
        shutil.copy2(ruta_db, ruta_nueva)
        return ruta_nueva
    return None

def generar_informe():
    _, _, GEN_DIR = get_paths()
    regs = get_registros()
    ram, modelo = get_ram_info()
    contenido = f"""INFORME GestorMasterS
Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}
{ram}
Modelo recomendado: {modelo}
----------------------------------------
"""
    for r in regs:
        contenido += f"📅 {r[3]} | 📂 {r[2]}\n{r[0]}: {r[1]}\n----------------------------------------\n"
    ruta_archivo = os.path.join(GEN_DIR, f"informe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)
    return ruta_archivo

# ==================== INICIO ====================
if __name__ == "__main__":
    init_db()
    print("✅ GestorMasterS cargado correctamente")
    print(get_ram_info())
