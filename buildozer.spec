[app]

# Título de tu app
title = GestorMasterS
package.name = gestormasters
package.domain = com.masterscorp.gestormasters

# Archivo principal
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json,ttf
source.include_patterns = assets/*,images/*,icon.png
source.exclude_exts = spec,md,gitignore,yml
source.exclude_dirs = bin,.buildozer,.git, __pycache__, CODIGO, DOCS,.github

version = 1.0
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

# Tu main
requirements = python3,kivy==2.3.1,kivymd==1.2.0,pillow,psutil,android
orientation = portrait
fullscreen = 0

# Icono
icon.filename = %(source.dir)s/icon.png

[buildozer]

# Log nivel 2 para ver todo
log_level = 2
warn_on_root = 1

# ESTO ES LO QUE ARREGLA TU ERROR DEL NDK 27
[app:android]

# Bootstrap obligatorio
p4a.bootstrap = sdl2
p4a.port = 8000

# SDK FIJO ESTABLE - NO 34, NO 37
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.buildtools = 33.0.2

# Acepta licencias automático
android.accept_sdk_license_agreements = True

# Arquitectura - solo 64 bits para que compile rápido
android.archs = arm64-v8a

# Permisos
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, VIBRATE

# Nombre del APK
android.ant = auto

# Para que no pida preview
android.use_legacy_storage = True

# Dejar que p4a no intente bajar NDK 27
p4a.ndk_version = 25b
p4a.sdk_version = 33
p4a.buildtools_version = 33.0.2

# Whitelist para que no meta librerías raras
# android.whitelist =

[app:ios]
# No lo usamos

[app:osx]
# No lo usamos
