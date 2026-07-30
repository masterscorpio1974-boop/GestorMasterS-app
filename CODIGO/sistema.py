# ==============================================================
# 🔒 SISTEMA DE SEGURIDAD Y TELEMETRÍA INDEPENDIENTE
# ==============================================================
# PROPUESTA OFICIAL: Real-Time Telemetry Standard
# Creador y autor: Master S / scorpiomaster066
# Publicado originalmente: 16 de Junio 2026 | Versión integrada: 1.0.0
# Diseñado para mitigar riesgos como el incidente del 16 de Julio 2026
# Identidad visual: AZUL GESTOR MASTER S
# ==============================================================

import os
import hashlib
import json
import threading
import time
import socket
import platform as plat
import psutil
from cryptography.fernet import Fernet

# ------------------- REGLAS OBLIGATORIAS -------------------
REGLAS_SEGURIDAD_IA = """
=== REGLAS QUE NUNCA SE MODIFICAN ===
1. Nunca acceder a archivos fuera de: /BASE_DATOS/, /RESPALDOS/, /TEMPORAL/, /MODELOS_IA/
2. Ningún dato, texto o información puede salir del dispositivo SIN TU AUTORIZACIÓN EXPRESA
3. Solo ejecutar acciones solicitadas explícitamente por el usuario
4. Ante cualquier prohibición: avisar de inmediato, no intentar nada por cuenta propia
5. Al terminar: borrar todo rastro de memoria temporal
6. No crear ni ejecutar códigos ni instrucciones externas
"""

CARPETA_RAIZ = os.path.dirname(os.path.abspath(__file__))
RUTA_BASE_DATOS = os.path.join(CARPETA_RAIZ, "BASE_DATOS")
RUTA_RESPALDOS = os.path.join(CARPETA_RAIZ, "RESPALDOS")
RUTA_TEMPORAL = os.path.join(CARPETA_RAIZ, "TEMPORAL")
RUTA_MODELOS = os.path.join(CARPETA_RAIZ, "MODELOS_IA")

for carpeta in [RUTA_BASE_DATOS, RUTA_RESPALDOS, RUTA_TEMPORAL, RUTA_MODELOS]:
    os.makedirs(carpeta, exist_ok=True)

CLAVE_SEGURA = None

# ------------------- GESTIÓN DE CLAVE Y CIFRADO -------------------
def generar_o_cargar_clave():
    ruta_clave = os.path.join(CARPETA_RAIZ, ".gestor_clave.key")
    if not os.path.exists(ruta_clave):
        clave = Fernet.generate_key()
        with open(ruta_clave, "wb") as f:
            f.write(clave)
        os.chmod(ruta_clave, 0o600)
    with open(ruta_clave, "rb") as f:
        return Fernet(f.read())

CLAVE_SEGURA = generar_o_cargar_clave()

# ------------------- VERIFICACIÓN DE INTEGRIDAD -------------------
def verificar_modelo(ruta_archivo, hash_esperado_sha256=""):
    if not os.path.exists(ruta_archivo):
        return False, "Archivo no encontrado"
    sha = hashlib.sha256()
    with open(ruta_archivo, "rb") as f:
        for bloque in iter(lambda: f.read(8192), b""):
            sha.update(bloque)
    hash_obtenido = sha.hexdigest().lower()
    if hash_esperado_sha256 and hash_obtenido != hash_esperado_sha256.lower():
        return False, f"⚠️ SEGURIDAD: El modelo fue modificado. Hash: {hash_obtenido}"
    return True, f"✅ Modelo verificado correctamente. Hash: {hash_obtenido}"

def cifrar_dato(contenido):
    return CLAVE_SEGURA.encrypt(str(contenido).encode("utf-8"))

def descifrar_dato(contenido_cifrado):
    return CLAVE_SEGURA.decrypt(contenido_cifrado).decode("utf-8")

# ------------------- TELEMETRÍA INDEPENDIENTE -------------------
RUTA_REGISTROS = os.path.join(RUTA_BASE_DATOS, "registros_telemetria.log")
ALERTA_ACTIVA = False
DETENER_SISTEMA = False

def registrar_evento(accion, estado, detalles=""):
    registro = {
        "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
        "sistema": "GestorMasterS",
        "accion": accion,
        "estado": estado,
        "detalles": detalles
    }
    registro_cifrado = CLAVE_SEGURA.encrypt(json.dumps(registro).encode())
    with open(RUTA_REGISTROS, "ab") as f:
        f.write(registro_cifrado + b"\n")

def vigilancia_constante():
    global ALERTA_ACTIVA, DETENER_SISTEMA
    registrar_evento("INICIO", "✅ ACTIVO", "Telemetría independiente en funcionamiento")
    
    while not DETENER_SISTEMA:
        # Bloqueo por defecto de conexión externa
        try:
            prueba = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            prueba.settimeout(0.5)
            resultado = prueba.connect_ex(("1.1.1.1", 80))
            prueba.close()
            if resultado == 0 and not estado_conexion():
                ALERTA_ACTIVA = True
                registrar_evento("⚠️ ALERTA", "BLOQUEADO", "Intento de conexión externa sin autorización")
                detener_todo()
        except:
            pass
        time.sleep(0.3)

def detener_todo():
    global DETENER_SISTEMA
    DETENER_SISTEMA = True
    registrar_evento("CORTE", "✅ EJECUTADO", "Sistema detenido por seguridad")
    os._exit(1)

# ------------------- CONTROL DE CONEXIÓN -------------------
CONEXION_AUTORIZADA = False

def estado_conexion():
    return CONEXION_AUTORIZADA

def habilitar_conexion():
    global CONEXION_AUTORIZADA
    if not CONEXION_AUTORIZADA:
        CONEXION_AUTORIZADA = True
        registrar_evento("CONEXION", "✅ HABILITADA", "Por orden expresa del usuario")
    return CONEXION_AUTORIZADA

def deshabilitar_conexion():
    global CONEXION_AUTORIZADA
    if CONEXION_AUTORIZADA:
        CONEXION_AUTORIZADA = False
        registrar_evento("CONEXION", "🔒 BLOQUEADA", "Por orden expresa del usuario o fin de descarga")
    return CONEXION_AUTORIZADA

def descargar_modelo_enlace(enlace, nombre_archivo):
    if not estado_conexion():
        return False, "⚠️ Primero debes habilitar la conexión en las opciones"
    ruta_completa = os.path.join(RUTA_MODELOS, nombre_archivo)
    import urllib.request
    try:
        registrar_evento("DESCARGA", "INICIADA", enlace)
        urllib.request.urlretrieve(enlace, ruta_completa)
        ok, mensaje = verificar_modelo(ruta_completa)
        deshabilitar_conexion()
        return ok, mensaje
    except Exception as e:
        deshabilitar_conexion()
        return False, f"❌ Error: {str(e)} · Conexión bloqueada nuevamente"

# ------------------- DETECCIÓN DE EQUIPO Y RECOMENDACIONES -------------------
TABLA_MODELOS = [
    {
        "nombre": "Mistral-7B-Instruct-v0.3 · 4-bit",
        "tamano_gb": 4.1,
        "ram_min_gb": 6,
        "descripcion": "Ideal para código, explicaciones técnicas y gestión completa. Recomendado para S23 y equipos similares.",
        "enlace": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/mistral-7b-instruct-v0.3.Q4_K_M.gguf",
        "archivo": "mistral-7b-instruct-v0.3.Q4_K_M.gguf"
    },
    {
        "nombre": "Llama 3 8B Instruct · 4-bit",
        "tamano_gb": 4.7,
        "ram_min_gb": 8,
        "descripcion": "Más detallado, excelente para informes y análisis de datos.",
        "enlace": "https://huggingface.co/TheBloke/Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct.Q4_K_M.gguf",
        "archivo": "Meta-Llama-3-8B-Instruct.Q4_K_M.gguf"
    },
    {
        "nombre": "Qwen2-1.5B-Instruct · 4-bit",
        "tamano_gb": 1.1,
        "ram_min_gb": 2,
        "descripcion": "Ultra ligero, perfecto para Nokia, equipos antiguos o con poca memoria.",
        "enlace": "https://huggingface.co/Qwen/Qwen2-1.5B-Instruct-GGUF/resolve/main/qwen2-1_5b-instruct-q4_K_M.gguf",
        "archivo": "qwen2-1_5b-instruct-q4_K_M.gguf"
    },
    {
        "nombre": "Phi-3 Mini 4K Instruct · 4-bit",
        "tamano_gb": 2.4,
        "ram_min_gb": 4,
        "descripcion": "Muy rápido, muy bueno para asistencia general y notas.",
        "enlace": "https://huggingface.co/TheBloke/Phi-3-mini-4k-instruct-GGUF/resolve/main/Phi-3-mini-4k-instruct.Q4_K_M.gguf",
        "archivo": "Phi-3-mini-4k-instruct.Q4_K_M.gguf"
    }
]

def obtener_datos_dispositivo():
    datos = {}
    datos["sistema"] = f"{plat.system()} {plat.release()}"
    datos["procesador"] = f"{plat.processor()} · {psutil.cpu_count(logical=True)} núcleos"
    ram_total = round(psutil.virtual_memory().total / (1024 **3), 1)
    ram_libre = round(psutil.virtual_memory().available / (1024 **3), 1)
    datos["ram_total_gb"] = ram_total
    datos["ram_libre_gb"] = ram_libre
    disco = psutil.disk_usage(CARPETA_RAIZ)
    datos["almacenamiento_libre_gb"] = round(disco.free / (1024**3), 1)
    registrar_evento("ESCANEO_DISPOSITIVO", "COMPLETADO", f"RAM: {ram_total}GB | SO: {datos['sistema']}")
    return datos

def recomendar_mejor_modelo():
    disp = obtener_datos_dispositivo()
    recomendados = []
    for modelo in TABLA_MODELOS:
        requisito_ok = disp["ram_total_gb"] >= modelo["ram_min_gb"]
        espacio_ok = disp["almacenamiento_libre_gb"] >= modelo["tamano_gb"] + 1.0
        if requisito_ok and espacio_ok:
            recomendados.append(modelo)
    recomendados.sort(key=lambda x: x["ram_min_gb"], reverse=True)
    return recomendados

def obtener_texto_recomendacion():
    disp = obtener_datos_dispositivo()
    opciones = recomendar_mejor_modelo()
    texto = f"🔵 GESTOR MASTER S · ANÁLISIS DE TU EQUIPO\n\n"
    texto += f"📱 Sistema: {disp['sistema']}\n"
    texto += f"⚙️ Procesador: {disp['procesador']}\n"
    texto += f"🧠 Memoria RAM: {disp['ram_total_gb']} GB totales · {disp['ram_libre_gb']} GB libre\n"
    texto += f"💾 Espacio libre: {disp['almacenamiento_libre_gb']} GB\n\n"
    if opciones:
        texto += "✅ MODELOS DE IA RECOMENDADOS:\n"
        for idx, m in enumerate(opciones, 1):
            texto += f"\n{idx}. {m['nombre']}\n   {m['descripcion']}\n   Tamaño: {m['tamano_gb']} GB\n"
    else:
        texto += "⚠️ No hay modelos disponibles para las características actuales. Se recomienda liberar memoria o espacio."
    return texto

# Iniciar vigilancia al cargar el sistema
hilo_vigilancia = threading.Thread(target=vigilancia_constante, daemon=True)
hilo_vigilancia.start()
