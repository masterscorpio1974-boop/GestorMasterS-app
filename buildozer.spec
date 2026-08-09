[app]
title = GestorMasterS
package.name = gestormasters
package.domain = org.test
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json
version = 2.0
requirements = hostpython3==3.11.9,python3==3.11.9,kivy==2.3.0,kivymd==1.1.1,cython==0.29.36,android,jnius,psutil
p4a.branch = master
orientation = portrait
[android]
android.ndk = 25b
android.sdk = 33
android.api = 33
android.minapi = 24
android.archs = arm64-v8a
android.apptheme =
android.allow_backup = True
android.buildtools = 33.0.2
android.accept_sdk_license = True
log_level = 2
warn_on_root_build = False
[buildozer]
log_level = 2
