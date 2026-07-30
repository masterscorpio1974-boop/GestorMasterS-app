[app]
title = GestorMasterS
package.name = gestormasters
package.domain = org.scorpiomaster

source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json,ttf
version = 1.0.0

# sqlite3 SE ELIMINA, se añade openssl que necesita cryptography
requirements = python3, kivy==2.3.0, kivymd==1.2.0, python-dateutil, cryptography, openssl, pillow
# pillow es requerido por kivy

orientation = portrait
fullscreen = 0
window_softinput_mode = resize

android.permissions = INTERNET
android.api = 33
android.minapi = 24
android.ndk = 25b
android.sdk = 33
android.archs = arm64-v8a
android.accept_sdk_license_agreement = True

# ESTO ES CLAVE
p4a.bootstrap = sdl2
p4a.local_recipes =
android.entrypoint = org.kivy.android.PythonActivity

[buildozer]
log_level = 2
warn_on_root = 0
