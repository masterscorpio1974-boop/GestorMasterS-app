3[app]
title = Gestor Master S
package.name = gestormastersapp
package.domain = com.masterscorpio.gestormasters

source.dir =.
source.include_exts = py,png,jpg,kv,atlas
version = 157.8
requirements = hostpython3==3.11.6,python3==3.11.6,kivy==2.3.1,kivymd==1.2.0,plyer,android,pyjnius
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION
android.api = 33
android.minapi = 24
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license_agreement = True
icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
