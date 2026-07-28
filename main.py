import os, shutil, sqlite3
from datetime import datetime
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView

def init_db():
 os.makedirs("BASE DE DATOS", exist_ok=True)
 os.makedirs("RESPALDOS", exist_ok=True)
 os.makedirs("ARCHIVOS GENERADOS", exist_ok=True)
 con=sqlite3.connect("BASE DE DATOS/datos.db")
 con.execute("CREATE TABLE IF NOT EXISTS info(id INTEGER PRIMARY KEY, tipo TEXT, texto TEXT, fecha TEXT)")
 con.commit(); con.close()

def add_info(tipo, texto):
 con=sqlite3.connect("BASE DE DATOS/datos.db")
 fecha=datetime.now().strftime("%Y-%m-%d %H:%M")
 con.execute("INSERT INTO info(tipo,texto,fecha) VALUES (?,?,?)",(tipo,texto,fecha))
 con.commit(); con.close()

def get_info(tipo):
 con=sqlite3.connect("BASE DE DATOS/datos.db")
 cur=con.cursor()
 cur.execute("SELECT texto,fecha FROM info WHERE tipo=? ORDER BY id DESC",(tipo,))
 d=cur.fetchall(); con.close()
 return d

def hacer_respaldo():
 o="BASE DE DATOS/datos.db"
 if os.path.exists(o):
  d=f"RESPALDOS/respaldo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
  shutil.copy(o,d); return d

def generar_informe():
 notas=get_info("nota"); tareas=get_info("tarea")
 txt=f"INFORME {datetime.now()}\nNotas:{len(notas)} Tareas:{len(tareas)}\n\n"
 for t,f in notas[:20]: txt+=f"[NOTA {f}] {t}\n"
 for t,f in tareas[:20]: txt+=f"[TAREA {f}] {t}\n"
 ruta=f"ARCHIVOS GENERADOS/Informe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
 os.makedirs("ARCHIVOS GENERADOS", exist_ok=True)
 open(ruta,"w",encoding="utf-8").write(txt)
 return ruta

KV='''
Screen:
 MDBoxLayout:
  orientation:'vertical'
  md_bg_color: 0.07,0.07,1
  padding:10
  spacing:10
  MDTextField:
   id: entrada
   hint_text: "Escribe nota o tarea..."
  MDBoxLayout:
   size_hint_y:None
   height:50
   spacing:10
   MDRaisedButton:
    text:"Guardar Nota"
    md_bg_color: 0,0.9,0.4,1
    on_release: app.guardar_nota()
   MDRaisedButton:
    text:"Guardar Tarea"
    md_bg_color: 1,0.6,0,1
    on_release: app.guardar_tarea()
  ScrollView:
   MDLabel:
    id: lista
    size_hint_y:None
    height: self.texture_size[1]
    text:"Sin datos"
  MDBoxLayout:
   size_hint_y:None
   height:50
   spacing:10
   MDRaisedButton:
    text:"Informe IA"
    on_release: app.hacer_informe()
   MDRaisedButton:
    text:"Respaldar"
    on_release: app.hacer_backup()
'''

class GestorApp(MDApp):
 def build(self):
  init_db()
  self.theme_cls.theme_style="Dark"
  return Builder.load_string(KV)
 def on_start(self):
  self.refresh()
 def refresh(self):
  t=""
  for txt,f in get_info("nota"): t+=f"[NOTA {f}] {txt}\n"
  for txt,f in get_info("tarea"): t+=f"[TAREA {f}] {txt}\n"
  self.root.ids.lista.text=t or "Vacio"
 def guardar_nota(self):
  if self.root.ids.entrada.text: add_info("nota",self.root.ids.entrada.text); self.root.ids.entrada.text=""; self.refresh()
 def guardar_tarea(self):
  if self.root.ids.entrada.text: add_info("tarea",self.root.ids.entrada.text); self.root.ids.entrada.text=""; self.refresh()
 def hacer_informe(self):
  generar_informe(); self.refresh()
 def hacer_backup(self):
  hacer_respaldo()

GestorApp().run()
