[app]
title = Gestor Master
package.name = gestormaster
package.domain = com.gestor.master
source.dir =.
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 30
android.ndk = 25b
android.accept_sdk_license_agreement = True

[buildozer]
log_level = 2
