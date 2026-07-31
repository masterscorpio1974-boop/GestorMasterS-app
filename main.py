from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from sistema import SistemaTelemetria

# Paleta de colores oscuros para preservación de energía
Window.clearcolor = (0, 0, 0, 1)

class GestorMasterSApp(App):
    def build(self):
        self.telemetria = SistemaTelemetria()
        
        # ScrollView principal para asegurar scroll en pantallas chicas de Android
        root = ScrollView(size_hint=(1, 1))
        self.contenedor = BoxLayout(orientation='vertical', padding=15, spacing=10, size_hint_y=None)
        self.contenedor.bind(minimum_height=self.contenedor.setter('height'))
        
        # Cabecera limpia
        self.contenedor.add_widget(Label(
            text="SISTEMA GESTOR MASTER S", 
            font_size='22sp', color=(0, 0.6, 1, 1), size_hint_y=None, height=45
        ))
        
        # Campos estructurados del Formulario de Contactos
        self.campos = {}
        campos_config = [
            ("nombre", "Nombre Completo"),
            ("telefono", "Telefono General"),
            ("celular", "Numero de Celular"),
            ("fijo", "Numero Fijo"),
            ("correo", "Correo Electronico"),
            ("direccion", "Direccion Residencial"),
            ("ubicacion", "Coordenadas o Enlace de Mapa"),
            ("nota", "Notas Especiales")
        ]
        
        for id_campo, placeholder in campos_config:
            txt_input = TextInput(
                hint_text=placeholder,
                background_color=(0.07, 0.07, 0.12, 1),
                foreground_color=(1, 1, 1, 1),
                hint_text_color=(0.4, 0.4, 0.4, 1),
                cursor_color=(0, 0.6, 1, 1),
                multiline=True if id_campo in ["direccion", "nota"] else False,
                size_hint_y=None,
                height=45 if id_campo not in ["direccion", "nota"] else 75
            )
            self.campos[id_campo] = txt_input
            self.contenedor.add_widget(txt_input)
            
        # Botones de Control Principal
        botones_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        
        btn_guardar = Button(text="GUARDAR DATOS", background_color=(0, 0.4, 0.9, 1), bold=True)
        btn_guardar.bind(on_press=self.procesar_guardado)
        
        btn_ver = Button(text="VER ALMACENADOS", background_color=(0.1, 0.5, 0.2, 1), bold=True)
        btn_ver.bind(on_press=self.mostrar_registros)
        
        botones_layout.add_widget(btn_guardar)
        botones_layout.add_widget(btn_ver)
        self.contenedor.add_widget(botones_layout)
        
        # Consola inteligente inferior para ver telemetría e informes de la IA
        self.consola = Label(
            text=self.telemetria.sugerir_modelo_ia(),
            font_size='13sp',
            color=(0, 0.8, 1, 1),
            halign='left',
            valign='top',
            size_hint_y=None,
            height=220
        )
        self.consola.bind(width=lambda *x: setattr(self.consola, 'text_size', (self.consola.width, None)))
        self.contenedor.add_widget(self.consola)
        
        root.add_widget(self.contenedor)
        return root

    def procesar_guardado(self, instance):
        datos_contacto = {id_c: input_w.text.strip() for id_c, input_w in self.campos.items()}
        
        if not datos_contacto["nombre"]:
            self.consola.text = "[ALERTA] El campo 'Nombre Completo' es obligatorio para guardar registros."
            return
            
        if self.telemetria.guardar_contacto_local(datos_contacto):
            self.consola.text = f"[OK] Datos de '{datos_contacto['nombre']}' asegurados en el almacenamiento local."
            for input_w in self.campos.values():
                input_w.text = ""
        else:
            self.consola.text = "[ERROR] Error al acceder a la base de datos local."

    def mostrar_registros(self, instance):
        contactos = self.telemetria.cargar_contactos()
        
        if not contactos:
            self.consola.text = "Base de datos vacia. No se encontraron contactos locales."
            return
            
        salida = f"{self.telemetria.sugerir_modelo_ia()}\n\n=== LISTA DE CONTACTOS EN DISCO ===\n"
        for i, c in enumerate(contactos, 1):
            salida += (
                f"[{i}] {c.get('nombre').upper()}\n"
                f"    Cel: {c.get('celular', '-')} | Tel: {c.get('telefono', '-')} | Fijo: {c.get('fijo', '-')}\n"
                f"    Email: {c.get('correo', '-')}\n"
                f"    Direccion: {c.get('direccion', '-')}\n"
                f"    Mapa: {c.get('ubicacion', '-')}\n"
                f"    Nota: {c.get('nota', '-')}\n"
                f"-----------------------------------\n"
            )
        self.consola.text = salida

if __name__ == '__main__':
    GestorMasterSApp().run()
