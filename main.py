import os, sqlite3, re
from datetime import datetime
from kivy.utils import platform
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase

class Tab(MDFloatLayout, MDTabsBase):
    pass

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
    os.makedirs(DB_DIR, exist_ok=True)
    return DB_DIR, "", ""

def init_db():
    DB_DIR, _, _ = get_paths()
    con = sqlite3.connect(os.path.join(DB_DIR,"datos.db"))
    con.execute("""CREATE TABLE IF NOT EXISTS registros(id INTEGER PRIMARY KEY AUTOINCREMENT,tipo TEXT, contenido TEXT, categoria TEXT, fecha TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS clientes(id INTEGER PRIMARY KEY AUTOINCREMENT,nombre TEXT, direccion TEXT, phone TEXT, correo TEXT,ubicacion TEXT, otros TEXT, fecha TEXT)""")
    con.commit()
    con.close()

def add_cliente(nombre, direccion, phone, correo, ubicacion, otros):
    DB_DIR, _, _ = get_paths()
    con = sqlite3.connect(os.path.join(DB_DIR,"datos.db"))
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    con.execute("INSERT INTO clientes(nombre,direccion,phone,correo,ubicacion,otros,fecha) VALUES (?,?,?,?,?,?,?)",(nombre, direccion, phone, correo, ubicacion, otros, fecha))
    con.commit()
    con.close()

def get_ram_info():
    ram_gb = 4.0
    try:
        if platform == 'android':
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            am = PythonActivity.mActivity.getSystemService(PythonActivity.ACTIVITY_SERVICE)
            ActivityManager = autoclass('android.app.ActivityManager')
            memInfo = ActivityManager.MemoryInfo()
            am.getMemoryInfo(memInfo)
            ram_gb = round(memInfo.totalMem / (1024**3), 1)
        else:
            import psutil
            ram_gb = round(psutil.virtual_memory().total / (1024**3), 1)
    except:
        pass
    if ram_gb < 2.5: sug = "qwen2:0.5b - Poca RAM"
    elif ram_gb < 4.5: sug = "qwen2:1.5b - Ideal"
    elif ram_gb < 7: sug = "qwen2.5:3b - Recomendado"
    else: sug = "qwen2.5:7b - Equipo potente"
    return f"{ram_gb} GB", sug

KV = '''
Screen:
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "GestorMasterS v2 OFFGRID"
        MDLabel:
            id: ram_label
            text: "Detectando RAM..."
            halign: "center"
            size_hint_y: None
            height: dp(40)
        MDTabs:
            Tab:
                title: "Clientes"
                BoxLayout:
                    orientation: 'vertical'
                    padding: dp(10)
                    spacing: dp(10)
                    MDTextField:
                        id: nombre
                        hint_text: "1. Nombre"
                    MDTextField:
                        id: direccion
                        hint_text: "2. Direccion"
                    MDTextField:
                        id: phone
                        hint_text: "3. Phone"
                    MDTextField:
                        id: correo
                        hint_text: "4. Correo"
                    MDTextField:
                        id: ubicacion
                        hint_text: "5. Ubicacion GPS"
                    MDTextField:
                        id: otros
                        hint_text: "6. Etc / Otros"
                    MDRaisedButton:
                        text: "GUARDAR CLIENTE OFFGRID"
                        pos_hint: {"center_x":.5}
                        on_release: app.guardar_cliente()
            Tab:
                title: "Info"
                MDLabel:
                    text: "100% OFFGRID - Detecta RAM y sugiere IA local"
                    halign: "center"
'''

class GestorMasterS(MDApp):
    def build(self):
        init_db()
        self.root = Builder.load_string(KV)
        ram, modelo = get_ram_info()
        self.root.ids.ram_label.text = f"{ram} | IA: {modelo}"
        return self.root
    def guardar_cliente(self):
        n = self.root.ids.nombre.text
        if n:
            add_cliente(n,self.root.ids.direccion.text,self.root.ids.phone.text,self.root.ids.correo.text,self.root.ids.ubicacion.text,self.root.ids.otros.text)
            self.root.ids.nombre.text = ""
            self.root.ids.direccion.text = ""
            self.root.ids.phone.text = ""
            self.root.ids.correo.text = ""
            self.root.ids.ubicacion.text = ""
            self.root.ids.otros.text = ""

if __name__ == "__main__":
    GestorMasterS().run()
