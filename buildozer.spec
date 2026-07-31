[app]
title = GestorMasterS
package.name = gestormasters
package.domain = com.masterscorp.gestormasters

source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json,ttf
source.include_patterns = assets/*,images/*,icon.png
source.exclude_exts = spec,md,gitignore,yml
source.exclude_dirs = bin,.buildozer,.git,__pycache__,CODIGO,DOCS,.github

version = 1.0

requirements = python3,kivy==2.3.1,kivymd==1.2.0,pillow,psutil,android
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
p4a.bootstrap = sdl2

# === RANGO ANDROID 10 HASTA 16 ===
android.minapi = 29
android.api = 35
android.sdk = 35
android.ndk = 26b
android.buildtools = 35.0.0

# Nombres fijos para p4a
p4a.minapi = 29
p4a.targetapi = 35
p4a.ndk_version = 26b
p4a.sdk_version = 35
p4a.buildtools_version = 35.0.0

# Fix para Android 16
android.accept_sdk_license_agreements = True
android.archs = arm64-v8a, armeabi-v7a
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, VIBRATE
android.ant = auto
android.use_legacy_storage = True
android.allow_backup = True

