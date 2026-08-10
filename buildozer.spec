[app]
title = Gestor Master S
package.name = gestormastersapp
package.domain = org.mastersorpiomaster
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
source.include_patterns = assets/*, *.json
version = 2.0
requirements = python3==3.11.8,hostpython3==3.11.8,kivy,kivymd,pyobjus;platform==MacOSX,plyer,pyjnius
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
