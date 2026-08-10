from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.lang import Builder
import os
import webbrowser
from kivy.utils import platform

def get_ram_gb():
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
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if "MemTotal" in line:
                        kb = int(line.split())
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
                source: "icon.png"  # Utiliza tu icon.png existente como logotipo superior con ojos brillantes
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
                            text: "VER REGISTROS LOCALES (.MD)"
                            pos_hint: {"center_x": .5}
                            text_color: 0, 0.7, 1, 1
                            line_color: 0, 0.7, 1, 1
                            on_release: app.ver_registros()

                        MDRaisedButton:
                            id: btn_download_ia
                            text: "DESCARGAR MODELO RECOMENDADO"
                            pos_hint: {"center_x": .5}
                            md_bg_color: 0.1, 0.1, 0.1, 1
                            text_color: 0, 0.9, 0.4, 1  # Destaca en verde para la descarga directa
                            on_release: app.descargar_ia()

                        MDLabel:
                            id: visor_datos
                            text: "Registros en Sistema\\nNo system entries recorded."
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 0, 0.7, 1, 1
                            adaptive_height: True
'''

class GestorMasterS(MDApp):
    ia_link = ""

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "LightBlue"
        return Builder.load_string(KV)

    def on_start(self):
        ram = get_ram_gb()
        if ram < 4.0:
            self.ia_link = "https://huggingface.co"
            info = f"{ram} GB | IA: qwen2:0.5b - Ultra Ligero"
            texto_btn = "DESCARGAR MODELO IA (qwen2:0.5b)"
        elif 4.0 <= ram < 6.0:
            self.ia_link = "https://huggingface.co"
            info = f"{ram} GB | IA: qwen2:1.5b - Ideal"
            texto_btn = "DESCARGAR MODELO IA (qwen2:1.5b)"
        elif 6.0 <= ram < 8.0:
            self.ia_link = "https://huggingface.co"
            info = f"{ram} GB | IA: qwen2:3b - Equilibrado"
            texto_btn = "DESCARGAR MODELO IA (qwen2:3b)"
        else:
            self.ia_link = "https://huggingface.co"
            info = f"{ram} GB | IA: qwen2:7b - Rendimiento Total"
            texto_btn = "DESCARGAR MODELO IA (qwen2:7b)"
            
        self.root.ids.label_ram.text = info
        self.root.ids.btn_download_ia.text = texto_btn

    def descargar_ia(self):
        if self.ia_link:
            webbrowser.open(self.ia_link)

    def guardar_cliente(self):
        nom = self.root.ids.nombre.text.strip()
        tel = self.root.ids.telefono.text.strip()
        dirr = self.root.ids.direccion.text.strip()
        corr = self.root.ids.correo.text.strip()
        
        if nom and tel:
            path_md = os.path.join(self.user_data_dir, 'datos_clientes.md')
            with open(path_md, 'a', encoding='utf-8') as f:
                f.write(f"## 🔹 Cliente: {nom}\n")
                f.write(f"* **Teléfono:** {tel}\n")
                f.write(f"* **Dirección:** {dirr if dirr else 'N/A'}\n")
                f.write(f"* **Correo:** {corr if corr else 'N/A'}\n")
                f.write("---\n\n")
                
            self.root.ids.nombre.text = ""
            self.root.ids.telefono.text = ""
            self.root.ids.direccion.text = ""
            self.root.ids.correo.text = ""
            self.root.ids.visor_datos.text = f"✅ Guardado en Markdown: {nom}"

    def ver_registros(self):
        path_md = os.path.join(self.user_data_dir, 'datos_clientes.md')
        if not os.path.exists(path_md) or os.path.getsize(path_md) == 0:
            texto = "Registros en Sistema\\nNo system entries recorded."
        else:
            with open(path_md, 'r', encoding='utf-8') as f:
                texto = f.read()
        self.root.ids.visor_datos.text = texto

if __name__ == '__main__':
    GestorMasterS().run()

