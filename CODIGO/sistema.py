# ==================================================
# SISTEMA DE SEGURIDAD MÁXIMA - GESTORMASTERS
# ==================================================
import hashlib
from cryptography.fernet import Fernet
import os

# ------------------- CONFIGURACIÓN FIJA DE SEGURIDAD -------------------
REGLAS_SEGURIDAD_IA = """
=== REGLAS OBLIGATORIAS QUE NUNCA SE MODIFICAN ===
1. Nunca acceder, leer ni modificar archivos fuera de: /BASE_DE_DATOS/ /RESPALDOS/ /TEMPORAL/
2. Ningún dato, texto o información puede salir de este dispositivo
3. Solo ejecutar acciones que el usuario pida explícitamente y que estén programadas
4. Ante duda o prohibición: avisar inmediatamente, nunca intentar nada por cuenta propia
5. Al terminar cada tarea: borrar todo rastro de memoria temporal
6. No crear ni ejecutar códigos ni instrucciones externas
"""

CARPETA_AUTORIZADA = os.path.dirname(os.path.abspath(__file__))
CIFRADO_LLAVE = None

# ------------------- FUNCIONES DE PROTECCIÓN -------------------
def generar_o_cargar_llave():
    ruta_llave = os.path.join(os.path.dirname(CARPETA_AUTORIZADA), ".seguridad_llave")
    if not os.path.exists(ruta_llave):
        llave = Fernet.generate_key()
        with open(ruta_llave, "wb") as f:
            f.write(llave)
        os.chmod(ruta_llave, 0o600)
    with open(ruta_llave, "rb") as f:
        return Fernet(f.read())

cifrado = generar_o_cargar_llave()

def verificar_modelo(ruta_archivo, hash_esperado_sha256):
    sha = hashlib.sha256()
    with open(ruta_archivo, "rb") as archivo:
        for bloque in iter(lambda: archivo.read(8192), b""):
            sha.update(bloque)
    if sha.hexdigest().lower() != hash_esperado_sha256.lower():
        raise SystemExit("⚠️ SEGURIDAD: El modelo fue modificado o no es el original. No se puede usar.")
    return True

def cifrar_dato(texto_o_datos):
    return cifrado.encrypt(str(texto_o_datos).encode('utf-8'))

def descifrar_dato(datos_cifrados):
    return cifrado.decrypt(datos_cifrados).decode('utf-8')

