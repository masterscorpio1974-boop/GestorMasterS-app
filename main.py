from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
import psutil

class Tab(MDFloatLayout, MDTabsBase):
    pass

KV = '''
MDScreen:
    md_bg_color: 0,0,0,1
    MDBoxLayout:
        orientation: 'vertical'
        MDBoxLayout:
            size_hint_y: None
            height: "160dp"
            orientation: 'vertical'
            padding: 15
            spacing: 5
            Image:
                source: "icon.png"
                size_hint: None, None
                size: "80dp","80dp"
                pos_hint: {"center_x": .5}
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
                            text: "Guardar Cliente OFFGRID"
                            pos_hint: {"center_x": .5}
                            on_release: app.guardar_cliente()
            Tab:
                title: "IA"
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: 15
                    spacing: 10
                    MDLabel:
                        id: ia_sugerencia
                        text: "IA: Analisis local..."
                        halign: "center"
                    MDLabel:
                        id: ia_descarga
                        text: ""
                        halign: "center"
                        theme_text_color: "Hint"
            Tab:
                title: "Ver Datos"
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: 20
                    spacing: 15
                    MDRaisedButton:
                        text: "MOSTRAR TODOS LOS REGISTROS"
                        pos_hint: {"center_x": .5}
                        on_release: app.ver_registros()
'''

class GestorMasterS(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        ram_gb = round(psutil.virtual_memory().total / (1024**3), 1)
        if ram_gb >= 8:
            modelo = "qwen2:7b - Rendimiento Total"
        elif ram_gb >= 6:
            modelo = "qwen2:3b - Equilibrado"
        elif ram_gb >= 4:
            modelo = "qwen2:1.5b - Ideal"
        else:
            modelo = "qwen2:0.5b - Ultra Ligero"
        self.root.ids.label_ram.text = f"{ram_gb} GB | IA: {modelo}"
        self.root.ids.ia_descarga.text = f"✅ Descarga recomendada: modelo local {modelo}"

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

    def ver_registros(self):
        pass

if __name__ == "__main__":
    GestorMasterS().run()
