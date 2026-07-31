[app]
title = GestorMasterS
package.name = gestormasters
package.domain = com.masterscorpio.gestormasters
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf
version = 1.0.0

requirements = hostpython3==3.11.9,python3==3.11.9,cython==0.29.36,kivy==2.3.1,kivymd==1.2.0,pillow

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk = 27c
android.build_tools_version = 34.0.0
android.accept_sdk_license_agreement = True
android.enable_androidx = True
p4a.bootstrap = sdl2
icon.filename = icon.png

[buildozer]
log_level = 2
warn_on_root = 1
