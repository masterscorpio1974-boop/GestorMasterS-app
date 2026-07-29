[app]
title = GestorMasterS
package.name = gestormasters
package.domain = org.scorpiomaster
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,md,txt
version = 1.0.0
requirements = python3==3.11.15, hostpython3==3.11.15, kivy==2.3.0, kivymd==1.2.0, markdown, libffi==3.4.6
android.recipe_python3 = 3.11.15
android.recipe_hostpython3 = 3.11.15
entrypoint = main.py
fullscreen = 0
orientation = portrait
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, READ_MEDIA_IMAGES, READ_MEDIA_VIDEO, READ_MEDIA_AUDIO
android.api = 34
android.ndk = 25b
android.build-tools = 30.0.3
android.archs = arm64-v8a
android.accept_sdk_license = True
android.enable_sdl2 = True
buildozer.allow_application_backup = True
android.use_aapt2 = True
android.skip_aidl_check = True
android.ndk_api = 24
android.recipe_libffi = 3.4.6
