[app]
title = GestorMasterS
package.name = gestormasters
package.domain = com.masterscorpio.gestormasters
source.dir =.
version = 1.0
requirements = python3==3.11.9,cython==0.29.36,kivy==2.3.1,kivymd==1.2.0,Pillow
orientation = portrait
android.permissions = INTERNET

[app:android]
android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk = 27c
android.accept_sdk_license_agreement = True
android.enable_androidx = True
p4a.bootstrap = sdl2
p4a.branch = master

[buildozer]
log_level = 2
