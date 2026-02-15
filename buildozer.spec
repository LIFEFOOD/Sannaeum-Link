[app]

# (str) Title of your application
title = 산내음 링크

# (str) Package name
package.name = sannaeeumlink

# (str) Package domain (needed for android/ios packaging)
package.domain = org.sannaeeum

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,ttf,txt

# (list) Source files to exclude
source.exclude_exts = spec

# (str) Application versioning
version = 0.1

# (list) Application requirements - 중요: 필요한 패키지 모두 명시
requirements = python3,kivy==2.2.1,pyjnius,android

# (str) Icon of the application
icon.filename = %(source.dir)s/res/drawable/icon.png

# (str) Supported orientation
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions - 중요: 저장소 권한 추가
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Automatically accept SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = armeabi-v7a

# (bool) Indicate that the application should be debuggable
android.debug = False

# (bool) Enable AndroidX support
android.use_androidx = True

# Gradle dependencies - 중요: AndroidX 코어 추가
android.gradle_dependencies = 'androidx.core:core:1.9.0'

# Gradle 데몬 메모리 설정
android.gradle_options = -Xmx1024M

# ===== APK 파일명 설정 =====
# (str) Filename for the release APK
android.filename = sannaeeum

# (str) Package format (apk or aab)
android.package_format = apk

# ===== 키스토어 설정 =====
# (str) Full path to the keystore
android.keystore = %(source.dir)s/sannaeeum.keystore

# (str) Keystore password
android.keystore_password = $(KEYSTORE_PASSWORD)

# (str) Keystore alias
android.keystore_alias = sannaeeum

# (str) Key password
android.key_password = $(KEY_PASSWORD)

# (bool) Indicate if it's a release build
android.release = True

# (str) The version of the build tools to use
android.build_tools = 33.0.2

# (str) The version of the NDK to use
android.ndk_version = 25.1.8937393

# (str) The p4a bootstrap to use
android.bootstrap = sdl2

# (str) Log level
log_level = 2

[buildozer]

# (int) Log level
log_level = 2

# (bool) Warn if the application is built as root
warn_on_root = 1
