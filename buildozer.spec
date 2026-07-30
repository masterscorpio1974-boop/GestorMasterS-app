[app]

# Título y datos básicos
title = GestorMasterS
package.name = gestormasters
package.domain = org.scorpiomaster
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,md,txt,json
version = 1.0.0

# Entorno y versiones EXACTAS compatibles
requirements = python3==3.11.9, hostpython3==3.11.9, kivy==2.3.0, kivymd==1.2.0, python-dateutil, cryptography, sqlite3
android.recipe_python3 = 3.11.9
android.recipe_hostpython3 = 3.11.9

# Configuración de pantalla
orientation = portrait
fullscreen = 0
window_softinput_mode = resize

# Seguridad SIN permisos innecesarios
android.permissions = INTERNET
android.allowBackup = False
android.debuggable = False

# Plataforma y compilación
android.api = 34
android.minapi = 34
android.ndk = 25b
android.archs = arm64-v8a

# Parches y arreglos de errores
android.buildtools = 30.0.3
android.accepts_license = True
buildozer.verbose = 1

# Arreglo definitivo del error ioctl/zip
android.entrypoint = main.py
android.add_assets = .
android.copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 0

# Variables para evitar entrada interactiva
env.PYTHONIOENCODING = utf-8
env.DEBIAN_FRONTEND = noninteractive
env.PYTHONUNBUFFERED = 1
