[app]
title = Gestor Master S
package.name = gestormasters
package.domain = com.masters.gestor
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0
requirements = hostpython3==3.11.8, python3==3.11.8, kivy==2.3.0, Cython==0.29.33, kivymd==1.2.0, pillow, materialyoucolor
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
android.permissions = INTERNET

[buildozer]
log_level = 2
