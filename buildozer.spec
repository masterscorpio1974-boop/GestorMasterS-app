[app]
title = GestorMasterS
package.name = gestormasters
package.domain = com.masterscorp.gestormasters
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json,ttf
source.include_patterns = assets/*,images/*,*.kv,icon.png
version = 1.0
requirements = python3,kivy==2.3.1,kivymd==1.2.0,pillow
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
p4a.bootstrap = sdl2
p4a.branch = master
android.minapi = 29
android.api = 35
android.sdk = 35
android.ndk = 26b
android.buildtools = 35.0.0
p4a.minapi = 29
p4a.targetapi = 35
p4a.ndk_version = 26b
p
