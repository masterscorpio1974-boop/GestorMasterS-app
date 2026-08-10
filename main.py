from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform
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
                        MDRaisedButton:
                            text: "Guardar Cliente"
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
                        text: "IA: Esperando analisis..."
                        halign: "center"
                    MDLabel:
                        id: ia_descarga
                        text: ""
                        halign: "center"
                        theme_text_color: "Hint"

            Tab:
                title
