from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatIconButton
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
import webbrowser
from kivy.utils import platform

def get_ram_gb():
    # En Android usamos la API del sistema para evitar fallos de permisos en /proc/meminfo
    if platform == 'android':
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = autoclass('android.content.Context')
            activity = PythonActivity.mActivity
            activity_manager = activity.getSystemService(Context.ACTIVITY_SERVICE)
            memory_info = autoclass('android.app.ActivityManager$MemoryInfo')()
            activity_manager.getMemoryInfo(memory_info)
            return round(memory_info.totalMem / (1024 * 1024 * 1024), 1)
        except Exception:
            return 4.0
    else:
        # Respaldo para pruebas locales en PC
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if "MemTotal" in line:
                        kb = int(line.split()[1])
                        return round(kb / 1024 / 1024, 1)
        except:
            return 4.0

class Tab(MDFloatLayout, MDTabsBase):
    pass

KV = '''
MDScreen:
    md_bg_color: 0, 0, 0, 1  # Fondo negro profundo
    
    MDBoxLayout:
        orientation: 'vertical'
        
        MDBoxLayout:
            size_hint_y: None
            height: "140dp"
            orientation: 'vertical'
            padding: 10
            spacing: 5
            
            Image:
                source: "logo.png"  # Muestra tu logo real con ojos brillantes
                size_hint: None, None
                size: "90dp", "90dp"
                pos_hint: {"center_x": .5}
                
            MDLabel:
                id: label_ram
                text: "Detectando RAM..."
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0, 0.7, 1, 1  # Azul Crystal
                font_style: "H6"
                
        MDTabs:
            id: tabs
            background_color: 0, 0.1, 0.2, 1
            tab_indicator_color: 0, 0.7, 1, 1
            
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
                            line_color_focus: 0, 0.7, 1, 1
                        MDTextField:
                            id: telefono
                            hint_text: "Teléfono"
                            line_color_focus: 0, 0.7, 1, 1
                        MDTextField:
                            id: direccion
                            hint_text: "Dirección"
                            line_color_focus: 0, 0.7, 1, 1
                        MDTextField:
                            id: correo
                            hint_text: "Correo"
                            line_color_focus: 0, 0.7, 1, 1
                            
                        MDRaisedButton:
                            text: "GUARDAR CLIENTE OFFGRID"
                            pos_hint: {"center_x": .5}
                            md_bg_color: 0, 0.5, 0.9, 1  # Azul Crystal Estilizado
                            on_release: app.guardar_cliente()
                            
                        MDRectangleFlatIconButton:
                            icon: "database-search"
                            text: "VER REGISTROS LOCALES"
                            pos_hint: {"center_x": .5}
                            text_color: 0, 0.7, 1, 1
                            line_color: 0, 0.7, 1, 1
                            on_release: app.ver_registros()

                        MDRaisedButton:
                            id: btn_download_ia
                            text: "DESCARGAR MODELO RECOMENDADO"
                            pos_hint: {"center_x": .5}
                            md_bg_color: 0.1, 0.1, 0.1, 1
                            text_color: 0, 0.9, 0.4, 1  # Verde para destacar la descarga
                            on_release: app.descargar_ia()

                        MDLabel:
                            id: visor_datos
                            text: "Registros en Sistema\\nNo system entries recorded."
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 0, 0.7, 1, 1
                            adaptive_height: True
                            padding: [0, 15]
'''

class GestorMasterS(MDApp):
    dialog = None
    ia_link = ""

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def on_start(self):
        ram = get_ram_gb()
        if ram < 4.0:
            self.ia_link = "https://huggingface.co"
            info = f"{ram} GB | IA: qwen2:0.5b - Ultra Ligero"
        elif 4.0 <= ram < 6.0:
            self.ia_link = "https://huggingface.co"
            info = f"{ram} GB | IA: qwen2:1.5b - Ideal"
        elif 6.0 <= ram < 8.0:
            self.ia_link = "https://huggingface.co"
            info = f"{ram} GB | IA: qwen2:3b - Equilibrado"
        else:
            self.ia_link = "https://huggingface.co"
            info = f"{ram} GB | IA: qwen2:7b - Rendimiento Total"
            
        self.root.ids.label_ram.text = info
        self.root.ids.btn_download_ia.text = f"DESCARGAR MODELO IA ({info.split(' | ')[1].replace('IA: ', '')})"

    def descargar_ia(self):
        if self.ia_link:
            webbrowser.open(self.ia_link)

    def guardar_cliente(self):
        store = JsonStore('datos_clientes.json')
        nom = self.root.ids.nombre.text.strip()
        tel = self.root.ids.telefono.text.strip()
        dirr = self.root.ids.direccion.text.strip()
        corr = self.root.ids.correo.text.strip()
        
        if nom and tel:
            store.put(nom, tel=tel, dir=dirr, mail=corr)
            self.root.ids.nombre.text = ""
            self.root.ids.telefono.text = ""
            self.root.ids.direccion.text = ""
            self.root.ids.correo.text = ""
            self.root.ids.visor_datos.text = f"✅ Guardado localmente: {nom}"

    def ver_registros(self):
        store = JsonStore('datos_clientes.json')
        if len(store) == 0:
            texto = "Registros en Sistema\\nNo system entries recorded."
        else:
            texto = "--- CLIENTES GUARDADOS OFFGRID ---\\n"
            for key in store.keys():
                data = store.get(key)
                texto += f"🔹 {key} | Tel: {data.get('tel','')}\\n"
        self.root.ids.visor_datos.text = texto

if __name__ == '__main__':
    GestorMasterS().run()

