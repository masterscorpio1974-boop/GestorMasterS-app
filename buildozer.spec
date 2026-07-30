[app]
title = GestorMasterS
package.name = gestormasters
package.domain = org.scorpiomaster
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0

requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow

orientation = portrait
fullscreen = 0
window_softinput_mode = resize
android.permissions = INTERNET

android.api = 34
android.minapi = 29
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.buildtools = 34.0.0
p4a.bootstrap = sdl2
android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
