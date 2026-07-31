import os
import shutil
import sqlite3
from datetime import datetime
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

def get_base_dir():
    app = MDApp.get_running_app()
    if app:
        return app.user_data_dir
    return os.path.abspath(".")

def get_path(*parts):
    base = get_base_dir()
    full = os.path.join(base, *parts)
    os.makedirs(os.path.dirname(full) if "." in parts[-1] else full, exist_ok=True)
    return full

def get_db_path():
    return get_path("DATA", "data.db")

def init_db():
    db_path = get_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    os.makedirs(get_path("BACKUPS"), exist_ok=True)
    os.makedirs(get_path("GENERATED_FILES"), exist_ok=True)
    con = sqlite3.connect(db_path)
    con.execute("CREATE TABLE IF NOT EXISTS entries(id INTEGER PRIMARY KEY, type TEXT, content TEXT, date TEXT)")
    con.commit()
    con.close()

def add_entry(entry_type, content):
    con = sqlite3.connect(get_db_path())
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    con.execute("INSERT INTO entries(type,content,date) VALUES (?,?,?)", (entry_type, content, current_date))
    con.commit()
    con.close()

def get_entries(entry_type):
    con = sqlite3.connect(get_db_path())
    cur = con.cursor()
    cur.execute("SELECT content,date FROM entries WHERE type=? ORDER BY id DESC", (entry_type,))
    result = cur.fetchall()
    con.close()
    return result

def create_backup():
    source_path = get_db_path()
    if os.path.exists(source_path):
        backup_name = get_path("BACKUPS", f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
        shutil.copy(source_path, backup_name)
        return backup_name
    return None

def generate_report():
    notes = get_entries("note")
    tasks = get_entries("task")
    report_text = f"REPORT {datetime.now()}\nNotes: {len(notes)} Tasks: {len(tasks)}\n\n"
    for content, date in notes[:20]:
        report_text += f"[NOTE {date}] {content}\n"
    for content, date in tasks[:20]:
        report_text += f"[TASK {date}] {content}\n"
    output_path = get_path("GENERATED_FILES", f"Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    return output_path

# REDISEÑO COMPLETO INTERFAZ NEÓN CYBERPUNK
LAYOUT = '''
MDScreen:
    md_bg_color: 0, 0, 0, 1  # Negro puro para resaltar el neón

    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)

        # Encabezado con Logo Estilo Escudo "S"
        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(160)
            spacing: dp(5)
            Image:
                source: 'icon.png'  # Asegúrate de que esté en la raíz de tu proyecto
                size_hint: (None, None)
                size: (dp(100), dp(100))
                pos_hint: {"center_x": .5}
            MDLabel:
                text: "Gestor Master S"
                halign: "center"
                font_style: "H5"
                bold: True
                theme_text_color: "Custom"
                text_color: 0, 0.64, 1, 1  # Azul Neón
            MDLabel:
                text: "Panel de control • Notas y Tareas"
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.5, 0.5, 0.5, 1

        # Campo de entrada estilizado oscuro con borde
        MDBoxLayout:
            size_hint_y: None
            height: dp(55)
            padding: [dp(10), 0, dp(10), 0]
            canvas.before:
                Color:
                    rgba: 0, 0.64, 1, 0.3  # Línea guía neón tenue
                Line:
                    width: 1.2
                    rounded_rectangle: (self.x, self.y, self.width, self.height, dp(8))
            TextInput:
                id: input_field
                hint_text: "Write note or task..."
                background_color: 0, 0, 0, 0
                foreground_color: 1, 1, 1, 1
                hint_text_color: 0.4, 0.4, 0.4, 1
                multiline: False
                cursor_color: 0, 0.64, 1, 1
                padding_y: [self.height / 2 - (self.line_height / 2), 0]

        # Botones Principales Superiores (Guardar con Bordes Redondeados)
        MDBoxLayout:
            size_hint_y: None
            height: dp(48)
            spacing: dp(15)
            MDFillRoundFlatButton:
                text: "  + Guardar Nota  "
                md_bg_color: 0, 0.5, 0.9, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.5
                on_release: app.save_note()
            MDFillRoundFlatButton:
                text: "  + Guardar Tarea  "
                md_bg_color: 0, 0.65, 1, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.5
                on_release: app.save_task()

        # Contenedor de Tarjetas de visualización (Efecto Contorno Neón)
        MDCard:
            orientation: "vertical"
            padding: dp(15)
            md_bg_color: 0.02, 0.05, 0.1, 0.6  # Azul profundo translúcido
            line_color: 0, 0.64, 1, 1  # Borde brillante Neón
            line_width: 1.5
            radius: [12, 12, 12, 12]
            
            MDLabel:
                text: "Registros en Sistema"
                font_style: "Subtitle1"
                bold: True
                theme_text_color: "Custom"
                text_color: 0, 0.75, 1, 1
                size_hint_y: None
                height: dp(25)
            
            MDSeparator:
                color: 0, 0.64, 1, 0.4

            ScrollView:
                bar_width: dp(4)
                MDLabel:
                    id: content_list
                    size_hint_y: None
                    height: self.texture_size[1]
                    text: "No data yet"
                    theme_text_color: "Custom"
                    text_color: 0.8, 0.9, 1, 1
                    font_style: "Body2"

        # Botones de Sistema Inferiores
        MDBoxLayout:
            size_hint_y: None
            height: dp(45)
            spacing: dp(15)
            MDRoundFlatButton:
                text: "Generate Report"
                text_color: 0, 0.64, 1, 1
                line_color: 0, 0.64, 1, 1
                size_hint_x: 0.5
                on_release: app.make_report()
            MDRoundFlatButton:
                text: "Backup Data"
                text_color: 0, 0.64, 1, 1
                line_color: 0, 0.64, 1, 1
                size_hint_x: 0.5
                on_release: app.make_backup()
'''

class GestorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        init_db()
        return Builder.load_string(LAYOUT)

    def on_start(self):
        self.refresh_list()

    def refresh_list(self):
        display_text = ""
        for content, date in get_entries("note"):
            display_text += f"▪ [NOTE {date}] {content}\n\n"
        for content, date in get_entries("task"):
            display_text += f"▪ [TASK {date}] {content}\n\n"
        self.root.ids.content_list.text = display_text or "No system entries recorded."

    def save_note(self):
        if self.root.ids.input_field.text.strip():
            add_entry("note", self.root.ids.input_field.text.strip())
            self.root.ids.input_field.text = ""
            self.refresh_list()

    def save_task(self):
        if self.root.ids.input_field.text.strip():
            add_entry("task", self.root.ids.input_field.text.strip())
            self.root.ids.input_field.text = ""
            self.refresh_list()

    def make_report(self):
        path = generate_report()
        self.refresh_list()

    def make_backup(self):
        create_backup()

if __name__ == '__main__':
    GestorApp().run()
