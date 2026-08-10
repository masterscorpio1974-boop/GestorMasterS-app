from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel

def get_ram_gb():
    try:
        with open('/proc/meminfo') as f:
            for line in f:
                if 'MemTotal' in line:
                    kb = int(line.split()[1])
                    return round(kb / 1024 / 1024, 1)
    except:
        return 4.0

class Tab(MDFloatLayout, MDTabsBase):
    pass

KV = '''
MDScreen:
    md_bg_color: 0,0,0,1
    MDBoxLayout:
        orientation: 'vertical'
        MDBoxLayout:
            size_hint_y: None
            height: "100dp"
            orientation: 'vertical'
            padding: 15
            spacing: 5
            Image:
                source: "icon.png"
                size_hint: None, None
                size: "80dp","80dp"
                pos_hint: {"center_x":.5}
            MDLabel:
                id: label_ram
                text: "Detectando RAM..."
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0,0.7,1,1
                        MDTabs:
            id: tabs
            Tab:
                title: "Clientes"
                MDScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: 15
                        spacing: 10
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
                        MDLabel:
                            id: visor_datos
                            text: "Sin datos"
                        MDLabel:
                            id: label_sugerencia
                            text: ""
                            halign: "center"
                        MDLabel:
                            id: ia_descarga
                            text: ""
                            halign: "center"
            Tab:
                title: "Ver Datos"
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: 20
                    spacing: 15
                    MDLabel:
                        text: "Registros en Sistema"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 0,0.7,1,1
                    MDRaisedButton:
                        text: "MOSTRAR TODOS LOS REGISTROS"
                        pos_hint: {"center_x":.5}
                        md_bg_color: 0,0.5,1,1
                        on_release: app.ver_registros()
                    MDLabel:
                        id: visor_datos2
                        text: "No system entries recorded."
                        halign: "left"
'''

class GestorMasterS(MDApp):
    dialog = None
    ia_link = ""

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def on_start(self):
        ram_gb = get_ram_gb()
        if ram_gb >= 8:
            modelo = "qwen2_7b - Rendimiento Total"
            self.ia_link = "https://huggingface.co/Qwen/Qwen2-7B-GGUF/resolve/main/qwen2-7b-instruct-q4_0.gguf"
        elif ram_gb >= 6:
            modelo = "qwen2_3b - Equilibrado"
            self.ia_link = "https://huggingface.co/Qwen/Qwen2-3B-GGUF/resolve/main/qwen2-3b-instruct-q4_0.gguf"
        elif ram_gb >= 4:
            modelo = "qwen2_1.5b - Ideal"
            self.ia_link = "https://huggingface.co/Qwen/Qwen2-1.5b-GGUF/resolve/main/qwen2-1.5b-instruct-q4_0.gguf"
        else:
            modelo = "qwen2_0.5b - Ultra Ligero"
            self.ia_link = "https://huggingface.co/Qwen/Qwen2-0.5B-GGUF/resolve/main/qwen2-0.5b-instruct-q4_0.gguf"
        self.root.ids.label_ram.text = f"{ram_gb} GB | IA: {modelo}"
        self.root.ids.label_sugerencia.text = f"Tu equipo: {ram_gb} GB RAM"
        self.root.ids.ia_descarga.text = f"Descarga recomendada: {modelo}\n{self.ia_link}"

    def guardar_cliente(self):
        nombre = self.root.ids.nombre.text.strip()
        tel = self.root.ids.telefono.text.strip()
        dirr = self.root.ids.direccion.text.strip()
        corr = self.root.ids.correo.text.strip()
        if nombre and tel:
            store = JsonStore("datos_clientes.json")
            store.put(nombre, tel=tel, dir=dirr, mail=corr)
            self.root.ids.nombre.text = ""
            self.root.ids.telefono.text = ""
            self.root.ids.direccion.text = ""
            self.root.ids.correo.text = ""
            self.root.ids.visor_datos.text = f"Guardado: {nombre}"

    def ver_registros(self):
        store = JsonStore("datos_clientes.json")
        if len(store) == 0:
            texto = "No system entries recorded."
        else:
            texto = ""
            for key in store.keys():
                data = store.get(key)
                texto += f"{key} | {data.get('tel','')} | {data.get('dir','')} | {data.get('mail','')}\n\n"
        self.root.ids.visor_datos2.text = texto

if __name__ == "__main__":
    GestorMasterS().run()
