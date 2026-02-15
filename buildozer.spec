[app]

# (str) Title of your application
title = 산내음 링크

# (str) Package name
package.name = sannaeeumlink

# (str) Package domain (needed for android/ios packaging)
package.domain = org.sannaeeum

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let everything but .git)
source.include_exts = py,png,jpg,kv,ttf,txt

# (list) Source files to exclude (e.g. you might don't want to upload your
source.exclude_exts = spec

# (list) List of directory to exclude from the source
#source.exclude_dirs = tests, bin

# (list) List of patterns to ignore
#source.exclude_patterns = license,images/*.jpg

# (str) Application versioning (method 1: manual version)
version = 0.1

# (list) Application requirements
requirements = python3,kivy

# (str) Icon of the application
icon.filename = %(source.dir)s/res/drawable/icon.png

# (str) Supported orientation
orientation = portrait

#
# OSX Specific
#
osx.python_version = 3
osx.kivy_version = 2.2.1

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Automatically accept SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = armeabi-v7a

# (bool) Indicate that the application should be debuggable
android.debug = False

# (bool) Enable AndroidX support
android.use_androidx = True

# Gradle 데몬 메모리 설정
android.gradle_options = -Xmx1024M

# ===== APK 파일로 빌드하도록 수정 =====
# (str) Package format (apk or aab) - apk로 변경!
android.package_format = apk

# (str) Filename for the release APK
android.filename = 산내음-링크

# ===== 키스토어 설정 =====
android.keystore = %(source.dir)s/sannaeeum.keystore
android.keystore_password = $(KEYSTORE_PASSWORD)
android.keystore_alias = sannaeeum
android.key_password = $(KEY_PASSWORD)

# (bool) Indicate if it's a release build
android.release = True

# (str) The version of the build tools to use
android.build_tools = 33.0.2

# (str) The version of the NDK to use
android.ndk_version = 25.1.8937393

# (str) The p4a bootstrap to use
android.bootstrap = sdl2

#
# Logging
#
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1
