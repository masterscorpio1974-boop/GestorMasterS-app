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
    # Crea la carpeta contenedora siempre
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

LAYOUT = '''
Screen:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.07, 0.07, 0.2, 1
        padding: dp(10)
        spacing: dp(10)
        MDTextField:
            id: input_field
            hint_text: "Write note or task..."
            mode: "fill"
        MDBoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            MDRaisedButton:
                text: "Save Note"
                md_bg_color: 0, 0.9, 0.4, 1
                on_release: app.save_note()
            MDRaisedButton:
                text: "Save Task"
                md_bg_color: 1, 0.6, 0, 1
                on_release: app.save_task()
        ScrollView:
            MDLabel:
                id: content_list
                size_hint_y: None
                height: self.texture_size[1]
                text: "No data yet"
        MDBoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            MDRaisedButton:
                text: "Generate Report"
                on_release: app.make_report()
            MDRaisedButton:
                text: "Backup Data"
                on_release: app.make_backup()
'''

class GestorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        init_db()
        return Builder.load_string(LAYOUT)

    def on_start(self):
        self.refresh_list()

    def refresh_list(self):
        display_text = ""
        for content, date in get_entries("note"):
            display_text += f"[NOTE {date}] {content}\n"
        for content, date in get_entries("task"):
            display_text += f"[TASK {date}] {content}\n"
        self.root.ids.content_list.text = display_text or "Empty"

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

GestorApp().run()
