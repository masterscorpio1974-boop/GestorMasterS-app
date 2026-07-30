[app]
title = GestorMasterS
package.name = gestormasters
package.domain = org.scorpiomaster
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,md,txt
version = 1.0.0

# VERSIONES SIN CONFLICTOS NUNCA MAS
requirements = python3==3.11.9, kivy==2.3.0, kivymd==1.2.0, markdown, requests, urllib3, idna, certifi, charset-normalizer, filetype

android.recipe_python3 = 3.11.9
android.recipe_hostpython3 = 3.11.9
android.recipe_libffi = 3.4.4
android.libffi_source = https://github.com/libffi/libffi/archive/refs/tags/v3.4.4.tar.gz

entrypoint = main.py
fullscreen = 0
orientation = portrait

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, READ_MEDIA_IMAGES, READ_MEDIA_VIDEO, READ_MEDIA_AUDIO

# USAMOS LO QUE YA EXISTE EN EL SISTEMA, SIN FORZAR VERSIONES QUE NO ESTAN
android.api = 34
android.ndk = 25c
android.api = 34
android.build-tools = 34.0.0
android.archs = arm64-v8a

android.accept_sdk_license = True
android.enable_sdl2 = True
buildozer.allow_application_backup = True
android.use_aapt2 = True
android.skip_aidl_check = True
android.ndk_api = 24
