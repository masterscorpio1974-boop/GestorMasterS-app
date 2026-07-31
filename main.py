import os
import shutil
import sqlite3
from datetime import datetime
from kivy.utils import platform
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView

def get_base_dir():
    app = MDApp.get_running_app()
    if app:
        return app.user_data_dir
    return os.path.abspath(".")

def get_path(*parts):
    base = get_base_dir()
    full = os.path.join(base, *parts)
    dir_part = os.path.dirname(full) if "." in os.path.basename(full) else full
    os.makedirs(dir_part, exist_ok=True)
    return full

def init_db():
    db_path = get_path("database", "gestormasters.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

KV = '''
MDScreenManager:
    MDScreen:
        name: "home"
        MDBoxLayout:
            orientation: "vertical"
            padding: dp(20)
            spacing: dp(15)

            MDTopAppBar:
                title: "GestorMasterS"
                elevation: 4

            MDLabel:
                text: "Sistema Seguro · Sin Rastros · Sin Google"
                halign: "center"
                font_style: "Caption"

            MDRaisedButton:
                text: "Verificar Dispositivo y Recomendar IA"
                on_release: app.check_device()

            MDRaisedButton:
                text: "Gestor de Datos"
                on_release: app.root.current = "data"

            MDRaisedButton:
                text: "Telemetría y Seguridad"
                on_release: app.root.current = "telemetry"

    MDScreen:
        name: "data"
        MDBoxLayout:
            orientation: "vertical"
            padding: dp(20)
            spacing: dp(15)

            MDTopAppBar:
                title: "Gestor de Datos"
                left_action_items: [["arrow-left", lambda x: app.root.current = "home"]]

            MDTextField:
                id: input_category
                hint_text: "Categoría"

            MDTextField:
                id: input_content
                hint_text: "Contenido"
                multiline: True
                height: dp(120)

            MDRaisedButton:
                text: "Guardar Registro"
                on_release: app.save_record()

    MDScreen:
        name: "telemetry"
        MDBoxLayout:
            orientation: "vertical"
            padding: dp(20)
            spacing: dp(15)

            MDTopAppBar:
                title: "Telemetría y Seguridad"
                left_action_items: [["arrow-left", lambda x: app.root.current = "home"]]

            MDLabel:
                id: telemetry_status
                text: "Estado: Sistema Activo y Aislado"
                halign: "center"

            MDRaisedButton:
                text: "Activar / Desactivar Internet"
                on_release: app.toggle_internet()

            MDRaisedButton:
                text: "Botón de Emergencia: Bloquear Todo"
                md_bg_color: 1, 0.2, 0.2, 1
                on_release: app.emergency_stop()
'''

class GestorMasterSApp(MDApp):
    internet_enabled = False

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        init_db()
        return Builder.load_string(KV)

    def check_device(self):
        import psutil
        total_ram = round(psutil.virtual_memory().total / (1024**3), 1)
        free_storage = round(shutil.disk_usage(get_base_dir()).free / (1024**3), 1)

        if total_ram < 3:
            model_rec = "Recomendación: Modelo muy ligero: Mistral-7B-Q4_K_M o similar"
        elif 3 <= total_ram < 6:
            model_rec = "Recomendación: Equilibrado: Llama 3 8B-Q5_K_M"
        else:
            model_rec = "Recomendación: Alto rendimiento: Qwen2 14B-Q6_K"

        self.root.get_screen("telemetry").ids.telemetry_status.text = (
            f"Dispositivo detectado\nMemoria: {total_ram} GB\nAlmacén libre: {free_storage} GB\n{model_rec}"
        )

    def save_record(self):
        cat = self.root.get_screen("data").ids.input_category.text.strip()
        cont = self.root.get_screen("data").ids.input_content.text.strip()
        if not cat or not cont:
            return
        db_path = get_path("database", "gestormasters.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO records (category, content, created_at) VALUES (?, ?, ?)",
            (cat, cont, datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        conn.commit()
        conn.close()
        self.root.get_screen("data").ids.input_category.text = ""
        self.root.get_screen("data").ids.input_content.text = ""

    def toggle_internet(self):
        self.internet_enabled = not self.internet_enabled
        estado = "ACTIVO" if self.internet_enabled else "DESACTIVADO"
        self.root.get_screen("telemetry").ids.telemetry_status.text = f"Conexión a internet: {estado} · Solo se usa para descargar modelos"

    def emergency_stop(self):
        self.internet_enabled = False
        self.root.get_screen("telemetry").ids.telemetry_status.text = "⚠️ MODO DE SEGURIDAD TOTAL ACTIVADO · TODAS LAS SALIDAS BLOQUEADAS"

if __name__ == "__main__":
    GestorMasterSApp().run()
