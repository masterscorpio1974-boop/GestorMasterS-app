import os
import shutil
import sqlite3
import psutil
from datetime import datetime
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog

# ==================== RUTAS Y BASE DE DATOS (TAL CUAL TU DISEÑO ORIGINAL) ====================
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
    report_text = f"INFORME GENERADO: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nNOTAS: {len(notes)} | TAREAS: {len(tasks)}\n\n"
    for content, date in notes[:20]:
        report_text += f"[NOTA · {date}] {content}\n"
    for content, date in tasks[:20]:
        report_text += f"[TAREA · {date}] {content}\n"
    output_path = get_path("GENERATED_FILES", f"Informe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    return output_path

# ==================== NUEVO: DETECCIÓN DE EQUIPO Y SUGERENCIA DE MODELO ====================
def detect_device_capabilities():
    try:
        total_ram_gb = round(psutil.virtual_memory().total / (1024 **3))
        free_storage_gb = round(shutil.disk_usage(get_base_dir()).free / (1024**3))
    except:
        total_ram_gb = 2
        free_storage_gb = 1

    if total_ram_gb >= 10 and free_storage_gb >= 8:
        return f"✅ Dispositivo: {total_ram_gb}GB RAM | {free_storage_gb}GB libres\n🔹 Recomendado: Mistral-7B-Instruct · Ideal para código, Termux y seguridad"
    elif total_ram_gb >= 6 and free_storage_gb >= 4:
        return f"✅ Dispositivo: {total_ram_gb}GB RAM | {free_storage_gb}GB libres\n🔹 Recomendado: Llama 3.2-3B · Equilibrado y muy capaz"
    elif total_ram_gb >= 3 and free_storage_gb >= 2:
        return f"✅ Dispositivo: {total_ram_gb}GB RAM | {free_storage_gb}GB libres\n🔹 Recomendado: Gemma-2B-it · Ligero y funcional"
    else:
        return f"✅ Dispositivo: {total_ram_gb}GB RAM | {free_storage_gb}GB libres\n🔹 Recomendado: modelos de 1B a 1.5B de parámetros"

def check_first_run():
    config_file = get_path("CONFIG", "inicializado.ok")
    if not os.path.exists(config_file):
        return True
    return False

def mark_initialized():
    with open(get_path("CONFIG", "inicializado.ok"), "w") as f:
        f.write(datetime.now().isoformat())

# ==================== INTERFAZ: TU DISEÑO NEÓN + TODOS LOS TEXTOS CORREGIDOS ====================
LAYOUT = '''
MDScreen:
    md_bg_color: 0, 0, 0, 1

    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)

        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(160)
            spacing: dp(5)
            Image:
                source: 'icon.png'
                size_hint: (None, None)
                size: (dp(100), dp(100))
                pos_hint: {"center_x": .5}
            MDLabel:
                text: "Gestor Master S"
                halign: "center"
                font_style: "H5"
                bold: True
                theme_text_color: "Custom"
                text_color: 0, 0.64, 1, 1
            MDLabel:
                text: "Panel de control • Notas y Tareas"
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.5, 0.5, 0.5, 1

        MDBoxLayout:
            size_hint_y: None
            height: dp(55)
            padding: [dp(10), 0, dp(10), 0]
            canvas.before:
                Color: rgba: 0, 0.64, 1, 0.3
                Line: width: 1.2, rounded_rectangle: (self.x, self.y, self.width, self.height, dp(8))
            TextInput:
                id: input_field
                hint_text: "Escribir nota o tarea..."
                background_color: 0, 0, 0, 0
                foreground_color: 1, 1, 1, 1
                hint_text_color: 0.4, 0.4, 0.4, 1
                multiline: False
                cursor_color: 0, 0.64, 1, 1
                padding_y: [self.height / 2 - (self.line_height / 2), 0]

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

        MDCard:
            orientation: "vertical"
            padding: dp(15)
            md_bg_color: 0.02, 0.05, 0.1, 0.6
            line_color: 0, 0.64, 1, 1
            line_width: 1.5
            radius: [12, 12, 12, 12]
            
            MDLabel:
                text: "Registros del Sistema"
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
                    text: "Sin entradas registradas aún"
                    theme_text_color: "Custom"
                    text_color: 0.8, 0.9, 1, 1
                    font_style: "Body2"

        MDBoxLayout:
            size_hint_y: None
            height: dp(45)
            spacing: dp(15)
            MDRoundFlatButton:
                text: "Generar Informe"
                text_color: 0, 0.64, 1, 1
                line_color: 0, 0.64, 1, 1
                size_hint_x: 0.5
                on_release: app.make_report()
            MDRoundFlatButton:
                text: "Respaldar Datos"
                text_color: 0, 0.64, 1, 1
                line_color: 0, 0.64, 1, 1
                size_hint_x: 0.5
                on_release: app.make_backup()
'''

# ==================== APLICACIÓN PRINCIPAL ====================
class GestorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        init_db()
        return Builder.load_string(LAYOUT)

    def on_start(self):
        self.refresh_list()
        # Solo muestra al abrir por PRIMERA VEZ
        if check_first_run():
            self.show_device_welcome()

    def show_device_welcome(self):
        info = detect_device_capabilities()
        self.dialog = MDDialog(
            title = "Bienvenido a Gestor Master S",
            text = f"{info}\n\nLa app funciona 100% sin conexión hasta que tú decidas descargar un modelo.",
            buttons = [
                MDRoundFlatButton(text="Entendido", on_release=lambda x: self.close_dialog())
            ]
        )
        self.dialog.open()

    def close_dialog(self):
        self.dialog.dismiss()
        mark_initialized()

    def refresh_list(self):
        display_text = ""
        for content, date in get_entries("note"):
            display_text += f"▪ [NOTA · {date}] {content}\n\n"
        for content, date in get_entries("task"):
            display_text += f"▪ [TAREA · {date}] {content}\n\n"
        self.root.ids.content_list.text = display_text or "Sin entradas registradas aún"

    def save_note(self):
        texto = self.root.ids.input_field.text.strip()
        if texto:
            add_entry("note", texto)
            self.root.ids.input_field.text = ""
            self.refresh_list()

    def save_task(self):
        texto = self.root.ids.input_field.text.strip()
        if texto:
            add_entry("task", texto)
            self.root.ids.input_field.text = ""
            self.refresh_list()

    def make_report(self):
        generate_report()
        self.refresh_list()

    def make_backup(self):
        create_backup()

if __name__ == '__main__':
    GestorApp().run()
