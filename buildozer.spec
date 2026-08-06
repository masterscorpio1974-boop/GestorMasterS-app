[app]
title = GestorMasterS
package.name = gestormasters
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3,kivy

orientation = portrait
oslog.python.level = INFO
oslog.android.level = INFO

python3 = python3.11
hostpython3 = python3.11

android.ndk = 25b
android.sdk = 24
android.api = 33
android.apptheme = @android:style/Theme.Holo.Light
android.arch = arm64-v8a,armeabi-v7a
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.allow_backup = True
android.minapi = 21
android.wakelock = False
android.fullscreen = False
android.use_aapt2 = True
android.buildtools = 33.0.0

presplash.filename = 
icon.filename = 

log_level = 2
warn_on_root_build = False
