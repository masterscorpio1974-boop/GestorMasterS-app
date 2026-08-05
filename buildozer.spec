[app]
title = GestorMasterS
package.name = gestormasters
package.domain = org.scorpiomaster
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf
version = 1.3.0

# VERSIONES COINCIDENTES SIN ERRORES
requirements = python3==3.11.9,kivy==2.3.1,kivymd==1.2.0,Pillow,pyjnius,plyer,requests,urllib3,charset-normalizer,idna,certifi

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.ndk = 27c
android.buildtools = 34.0.0
android.accept_sdk_license_agreement = True
android.enable_androidx = True
p4a.bootstrap = sdl2
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 0
