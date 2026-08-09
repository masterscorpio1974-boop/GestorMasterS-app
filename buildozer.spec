[app]
title = Gestor Master S
package.name = gestormasters
package.domain = com.masters.gestor
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 21
android.ndk = 23b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

# ESTO ES LO QUE TE FALTA PARA QUE NO TRUENE LIBFFI
p4a.fork = kivy
p4a.branch = develop
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
