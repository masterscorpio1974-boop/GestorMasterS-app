[app]
title = GestorMasterS
package.name = gestormasters
package.domain = com.masterscorpio.gestormasters
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,md,gguf
version = 1.0.0

requirements = python3==3.11.15, hostpython3==3.11.15, kivy==2.3.0, kivymd==1.2.0, cryptography==42.0.8, psutil==5.9.8

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.allowBackup = False
android.debuggable = False
android.minapi = 33
android.api = 34
android.ndk = 25b
android.archs = arm64-v8a

android.accept_license_agreement = True
android.enable_androidx = True
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
android.buildozer_verbose = 1
