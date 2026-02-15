[app]

# (str) Title of your application
title = 산내음 링크

# (str) Package name
package.name = sannaeeumlink

# (str) Package domain
package.domain = org.sannaeeum

# (str) Source code directory
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,ttf,txt

# (list) Source files to exclude
source.exclude_exts = spec

# (str) Application version
version = 0.1

# (list) Application requirements - 최소 요구사항
requirements = python3,kivy==2.1.0

# (str) Icon of the application
icon.filename = %(source.dir)s/res/drawable/icon.png

# (str) Supported orientation
orientation = portrait

#
# Android specific
#

# (bool) Fullscreen
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 31

# (int) Minimum API
android.minapi = 21

# (str) Android NDK version
android.ndk = 23b

# (bool) Automatically accept SDK license
android.accept_sdk_license = True

# (str) Android architectures - 단일 아키텍처
android.archs = armeabi-v7a

# (bool) Debug mode
android.debug = False

# (bool) Enable AndroidX support
android.use_androidx = True

# Gradle dependencies - 제거 (문제 발생 시)
# android.gradle_dependencies =

# Gradle options
android.gradle_options = -Xmx1024M

# (str) Package format
android.package_format = apk

# (str) Keystore settings
android.keystore = %(source.dir)s/sannaeeum.keystore
android.keystore_password = $(KEYSTORE_PASSWORD)
android.keystore_alias = sannaeeum
android.key_password = $(KEY_PASSWORD)

# (bool) Release build
android.release = True

# (str) Build tools version
android.build_tools = 30.0.3

# (str) NDK version
android.ndk_version = 23.1.7779620

# (str) Bootstrap
android.bootstrap = sdl2

# (str) Log level
log_level = 2

# 추가: 안드로이드 아티팩트 설정
android.add_src = 

[buildozer]

# (int) Log level
log_level = 2

# (bool) Warn if built as root
warn_on_root = 1
