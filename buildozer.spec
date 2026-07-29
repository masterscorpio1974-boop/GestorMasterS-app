[app]
title = GestorMasterS
package.name = gestormasters
package.domain = org.scorpiomaster
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,md,txt
version = 1.0.0
requirements = python3, kivy==2.3.0, kivymd==1.2.0, markdown, cryptography
entrypoint = main.py
fullscreen = 0
orientation = portrait

# Permisos completos
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES, READ_MEDIA_VIDEO, READ_MEDIA_AUDIO

# Versiones probadas y compatibles
android.api = 34
android.ndk = 25b
android.build-tools = 30.0.3
android.accepts_license = True
android.archs = arm64-v8a
android.enable_sdl2 = True

# Opciones importantes para que no falle
buildozer.allow_application_backup = True
android.gradle_dependencies = ''
android.use_aapt2 = True
