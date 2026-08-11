from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.lang import Builder
from kivy.utils import platform
import os

def get_ram_gb():
    if platform == 'android':
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = autoclass('android.content.Context')
            activity = PythonActivity.mActivity
            am = activity.getSystemService(Context.ACTIVITY_SERVICE)
            mi = autoclass('android.app.ActivityManager$MemoryInfo')()
            am.getMemoryInfo(mi)
            return round(mi.totalMem / (1024**3), 1)
        except:
            return 4.0
    else:
        return 4.0

class Tab(MDFloatLayout, MDTabsBase):
    pass

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        MDLabel:
            id: label_ram
            text: "Detectando RAM..."
            halign: "center"
            size_hint_y: None
            height: "50dp"
        MDTabs:
            id: tabs
            Tab:
                title: "Clientes"
                MDScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: 20
                        spacing: 15
                        adaptive_height: True
                        MDTextField:
                            id: nombre
                            hint_text: "Nombre Cliente"
                        MDTextField:
                            id: telefono
                            hint_text: "Telefono"
                        MDTextField:
                            id: direccion
                            hint_text: "Direccion"
                        MDTextField:
                            id: correo
                            hint_text: "Correo"
                        MDRaisedButton:
                            text: "GUARDAR CLIENTE"
                            pos_hint: {"center_x":.5}
                            on_release: app.guardar_cliente()
                        MDRectangleFlatIconButton:
                            text: "VER REGISTROS"
                            pos_hint: {"center_x":.5}
                            on_release: app.ver_registros()
                        MDRaisedButton:
                            id: btn_download_ia
                            text: "DESCARGAR IA"
                            pos_hint: {"center_x":.5}
                            on_release: app.descargar_ia()
                        MDLabel:
                            id: visor_datos
                            text: "Sin registros"
                            adaptive_height: True
'''

class GestorMasterS(MDApp):
    ia_link = ""
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)
    def on_start(self):
        ram = get_ram_gb()
        self.ia_link = "https://huggingface.co/Qwen/Qwen2-0.5B-GGUF/resolve/main/qwen2-0.5b-instruct-q4_0.gguf"
        self.root.ids.label_ram.text = f"{ram} GB | IA: 0.5b Ligero"
    def descargar_ia(self):
        self.root.ids.visor_datos.text = self.ia_link
    def guardar_cliente(self):
        nom = self.root.ids.nombre.text.strip()
        if not nom:
            self.root.ids.visor_datos.text = "Pon nombre"
            return
        ruta = "/sdcard/Download/clientes.md"
        try:
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
        except:
            pass
        with open(ruta, "a", encoding="utf-8") as f:
            f.write(f"- {nom}\n")
        self.root.ids.visor_datos.text = f"Guardado: {nom}"
    def ver_registros(self):
        ruta = "/sdcard/Download/clientes.md"
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                self.root.ids.visor_datos.text = f.read()
        else:
            self.root.ids.visor_datos.text = "No hay registros"

if __name__ == '__main__':
    GestorMasterS().run()
