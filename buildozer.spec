[app]
title = GestorMasterS v2 OFFGRID
package.name = mastersgestor
package.domain = com.mastersgrid.offgrid
source.dir = .
source.include_exts = py,png,kv,json,db
version = 1.0

requirements = python3,
    kivy==2.3.0,
    kivymd==2.0.0,
    materialyoucolor,
    materialshapes,
    pycairo,
    pillow,
    asynckivy,
    psutil,
    cython==0.29.37

orientation = portrait
icon.filename = %(source.dir)s/icon.png
android.icon = %(source.dir)s/icon.png
android.icon_round = %(source.dir)s/icon.png
preserve_assets = *.png, *.kv, *.json, *.db
p4a.bootstrap = sdl2

# ✅ LO QUE ARREGLABA Y FALTABA:
android.build_tools_version = "34.0.0"
android.accept_sdk_license_agreement = True

[buildozer]
log_level = 2

[app:android]
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = r25b
android.features = android.hardware.touchscreen
