[app]
title = Gestor Master S
package.name = gestormasters
package.domain = com.masters.gestor
source.dir =.
source.include_exts = py,png,jpg,kv,atlas
version = 1.2
requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow
orientation = portrait
android.api = 33
android.minapi = 21
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.accept_sdk_license_agreement = True
fullscreen = 0

[buildozer]
log_level = 2
