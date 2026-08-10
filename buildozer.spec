[app]
title = MasterS Gestor
package.name = mastersgestor
package.domain = com.masters.offgrid

source.dir =.
source.include_exts = py,png,jpg,kv,json
version = 1.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,psutil
orientation = portrait
icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2

[app:android]
# Necesario para que no se cierre al pedir permisos
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license_agreement = True
# Para que funcione el almacenamiento
android.features = android.hardware.touchscreen
# Deja que python use tu logo
p4a.bootstrap = sdl2

[buildozer:android]
# Si compilas en Colab / Linux
# buildozer android debug
