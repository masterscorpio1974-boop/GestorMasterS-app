[app]
title = GestorMasterS
package.name = gestormasters
package.domain = org.scorpiomaster
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow
orientation = portrait
fullscreen = 0
window_softinput_mode = resize
android.permissions = INTERNET

# ANDROID 10 (API 29) hasta ANDROID 16 (API 36)
android.api = 36
android.minapi = 29
android.sdk = 36
android.ndk = 28b
android.archs = arm64-v8a, armeabi-v7a
p4a.bootstrap = sdl2
android.accept_sdk_license_agreement = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
