[app]
title = GestorMasterS
package.name = gestormasters
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
# ✅ VERSIONES EXACTAS Y COMPATIBLES ENTRE SI
requirements = python3==3.10, kivy==2.3.0, cython==0.29.37
orientation = portrait

[app:p4a]
p4a.branch = v2024.07.08
p4a.bootstrap = sdl2
android.ndk = 25b
android.sdk = 33
android.api = 33
android.minapi = 24
android.arch = arm64-v8a
android.apptheme = @android:style/Theme.Holo.Light
# ✅ QUITAMOS INTERNET SI ES 100% OFFLINE
# android.permissions = INTERNET
android.allow_backup = True
android.buildtools = 33.0.2

presplash.filename =
icon.filename =
log_level = 2
warn_on_root_build = False
