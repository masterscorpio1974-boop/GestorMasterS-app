[app]
title = Gestor Master S
package.name = gestormastersapp
package.domain = org.mastersorpiomaster
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,ttf,json,md
source.include_patterns = assets/*,*.json,*.md
version = 2.0
requirements = hostpython3==3.11.8,python3==3.11.8,kivy==3.0.0,kivymd==1.2.0,plyer,android,pyjnius
icon.filename = %(source.dir)s/icon.png
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
