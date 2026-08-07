[app]

# (str) Title of your application
title = GestorMaster5

# (str) Package name
package.name = gestormasters

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# Ensure it matches your workflow EXACTLY

requirements = python3==3.11,kivy==2.3.0,cython==0.29.36
p4a.branch = master


# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# =============================================================================
# Android specific
# =============================================================================

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android SDK version to use
android.sdk = 33

# (int) Android API to target
android.api = 33

# (int) Minimum API required
android.minapi = 24

# (str) Android architecture to build for
android.archs = arm64-v8a

# (str) Android application theme
android.apptheme = @android:style/Theme.Holo.Light

# (bool) Allow backup
android.allow_backup = True

# (str) Android build tools version to use
android.buildtools = 33.0.2

# (bool) If True, then automatically accept SDK license agreements.
# ESTA ES LA LÍNEA MÁGICA QUE EVITA QUE SE DETENGA EL WORKFLOW
android.accept_sdk_license = True

# =============================================================================
# Python for android (p4a) specific
# =============================================================================

# (str) python-for-android branch to use
p4a.branch = v2024.07.08

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2


# =============================================================================
# Display settings
# =============================================================================

# (str) Presplash filename
presplash.filename =

# (str) Icon filename
icon.filename =

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (bool) Give a warning if the build is run as root
warn_on_root_build = False
