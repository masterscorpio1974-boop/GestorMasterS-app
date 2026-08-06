[app]
title = GestorMasterS
package.name = gestormasters
package.domain = org.test
source.dir =.
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3==3.11.8,kivy==2.3.0
orientation = portrait

[app:p4a]
p4a.branch = master
p4a.bootstrap = sdl2
android.ndk = 25b
android.sdk = 33
android.api = 33
android.minapi = 21
android.arch = arm64-v8a
android.apptheme = @android:style/Theme.Holo.Light
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.allow_backup = True
android.wakelock = False
android.fullscreen = False
android.use_aapt2 = True
android.buildtools = 33.0.2

presplash.filename =
icon.filename =
log_level = 2
warn_on_root_build = False
