[app]
title = GestorMasterS
package.name = gestormasters
package.domain = org.scorpiomaster

source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json,txt,db
source.include_patterns = main.py, CODIGO/*.py, BASE_DE_DATOS/*, ARCHIVOS_GENERADOS/*, RESPALDOS/*
source.exclude_dirs = bin,.buildozer,.git,.github,downloads,go,storage,Real-Time-Telemetry-Standard,phoneinfoga
source.exclude_patterns = phoneinfoga*, *.tar.gz, modelfile, Modelfile

version = 2.0
version.regex = __version__ = ['"]([^'"]*)['"]
version.filename = main.py

requirements = python3,kivy==2.3.0,kivymd==1.2.0

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
p4a.branch = master
p4a.bootstrap = sdl2
p4a.port = 8000

android.api = 33
android.minapi = 24
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license_agreements = True

# OFFGRID - Sin internet
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.features = android.hardware.touchscreen

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png
