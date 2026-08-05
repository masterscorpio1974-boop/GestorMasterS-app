import os, shutil, sqlite3
from datetime import datetime
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform

def get_base_dir():
    # En Android usa la carpeta privada donde SI deja guardar
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
    con.execute("""CREATE TABLE IF NOT EXISTS clientes(
        id INTEGER PRIMARY KEY,
        nombre TEXT, telefono TEXT, direccion TEXT,
        correo TEXT, ubicacion TEXT, otros TEXT, fecha TEXT)""")
    con.commit(); con.close()

def add_cliente(d):
    DB_DIR, _, _ = get_paths()
    con=sqlite3.connect(os.path.join(DB_DIR,"datos.db"))
    fecha=datetime.now().strftime("%Y-%m-%d %H:%M")
    con.execute("INSERT INTO clientes(nombre,telefono,direccion,correo,ubicacion,otros,fecha) VALUES (?,?,?,?,?,?,?)",
                (d['nombre'],d['telefono'],d['direccion'],d['correo'],d['ubicacion'],d['otros'],fecha))
    con.commit(); con.close()

def get_clientes():
    DB_DIR, _, _ = get_paths()
    con=sqlite3.connect(os.path.join(DB_DIR,"datos.db"))
    cur=con.cursor()
    cur.execute("SELECT nombre,telefono,direccion,correo,ubicacion,otros,fecha FROM clientes ORDER BY id DESC")
    data=cur.fetchall(); con.close()
    return data

def hacer_respaldo():
    DB_DIR, RESP_DIR, _ = get_paths()
    o=os.path.join(DB_DIR,"datos.db")
    if os.path.exists(o):
        d=os.path.join(RESP_DIR,f"respaldo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
        shutil.copy(o,d); return d

def generar_informe():
    _, _, GEN_DIR = get_paths()
    clientes=get_clientes()
    txt=f"INFORME OFFGRID GestorMasterS - {datetime.now()}\nTotal clientes:{len(clientes)}\n{'='*40}\n\n"
    for n,t,di,c,u,o,f in clientes:
        txt+=f"1.Nombre: {n}\n2.Telefono: {t}\n3.Direccion: {di}\n4.Correo: {c}\n5.Ubicacion: {u}\n6.Otros: {o}\nFecha:{f}\n{'-'*30}\n"
    ruta=os.path.join(GEN_DIR,f"Informe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    open(ruta,"w",encoding="utf-8").write(txt)
    return ruta

KV='''
Screen:
    MDBoxLayout:
        orientation:'vertical'
        padding:10
        spacing:8
        MDLabel:
            text: "GestorMasterS OFFGRID - YA GUARDA"
            halign: "center"
            font_style: "H6"
            size_hint_y: None
            height: 35
        ScrollView:
            size_hint_y: None
            height: 340
            MDBoxLayout:
                orientation:'vertical'
                spacing:8
                adaptive_height: True
                MDTextField:
                    id: nombre
                    hint_text: "1. Nombre"
                MDTextField:
                    id: telefono
                    hint_text: "2. Telefono"
                MDTextField:
                    id: direccion
                    hint_text: "3. Direccion"
                MDTextField:
                    id: correo
                    hint_text: "4. Correo"
                MDTextField:
                    id: ubicacion
                    hint_text: "5. Ubicacion (link maps)"
                MDTextField:
                    id: otros
                    hint_text: "6. Otros"
                    multiline: True
        MDBoxLayout:
            size_hint_y:None
            height:50
            spacing:10
            MDRaisedButton:
                text:"Guardar Cliente"
                on_release: app.guardar_cliente()
            MDRaisedButton:
                text:"Limpiar"
                on_release: app.limpiar()
        ScrollView:
            MDLabel:
                id: lista
                size_hint_y:None
                height: self.texture_size[1]
                text:"Sin datos OFFGRID"
        MDBoxLayout:
            size_hint_y:None
            height:50
            spacing:10
            MDRaisedButton:
                text:"Informe"
                on_release: app.hacer_informe()
            MDRaisedButton:
                text:"Respaldar"
                on_release: app.hacer_backup()
'''

class GestorApp(MDApp):
    def build(self):
        init_db()
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="Blue"
        return Builder.load_string(KV)
    def on_start(self): self.refresh()
    def refresh(self):
        t=""
        for n,tel,di,c,u,o,f in get_clientes():
            t+=f"[{f}] {n} | {tel} | {u}\n"
        self.root.ids.lista.text=t or "Vacio - OFFGRID"
    def limpiar(self):
        for i in ['nombre','telefono','direccion','correo','ubicacion','otros']:
            self.root.ids[i].text=""
    def guardar_cliente(self):
        datos={k:self.root.ids[k].text.strip() for k in ['nombre','telefono','direccion','correo','ubicacion','otros']}
        if not datos['nombre']: return
        add_cliente(datos); self.limpiar(); self.refresh()
    def hacer_informe(self):
        r=generar_informe()
        print(f"Informe en {r}")
        self.refresh()
    def hacer_backup(self):
        r=hacer_respaldo()
        print(f"Respaldo en {r}")
        self.refresh()

GestorApp().run()
