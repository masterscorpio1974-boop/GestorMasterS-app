[app]
title = GestorMasterS
package.name = gestormasters
package.domain = org.scorpiomaster
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,md,txt
version = 1.0.0

requirements = hostpython3==3.11.9, python3==3.11.9, kivy==2.3.0, kivymd==1.2.0, pillow, markdown, requests, urllib3, idna, certifi, charset-normalizer, filetype
entrypoint = main.py
fullscreen = 0
orientation = portrait

android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 34
android.accept_sdk_license = True
android.archs = arm64-v8a
