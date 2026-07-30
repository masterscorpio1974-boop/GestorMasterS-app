[app]
title = GestorMasterS
package.name = gestormasters
package.domain = com.masterscorpio.gestormasters
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json,db,txt
version = 1.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,sqlite3,Pillow
orientation = portrait
fullscreen = 0
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
# Esto es lo que te estaba tronando, solo 64 bits
android.archs = arm64-v8a
p4a.branch = master
# Android 16 = API 36
android.api = 36
android.minapi = 21
android.ndk = 27c
android.sdk = 36
android.accept_sdk_license_agreement = True
android.ant = auto
# Para que jale bien en One UI 8.5
android.enable_androidx = True
android.allow_backup = True
p4a.bootstrap = sdl2
