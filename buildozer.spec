[app]
title = GestorMasterS v2 OFFGRID
package.name = mastersgestor
package.domain = com.mastersgrid.offgrid
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 2.0

requirements = python3,kivy==2.3.0,kivymd==1.1.1,psutil,plyer,android

orientation = portrait
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.build_tools_version = "34.0.0"
android.accept_sdk_license_agreement = True
p4a.bootstrap = sdl2
android.archs = arm64-v8a, armeabi-v7a
android.features = android.hardware.touchscreen
