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
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
requirements = python3,kivy,pyjnius

# (str) Presplash of the application
presplash.filename = %(source.dir)s/res/drawable/presplash.png

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
fullscreen = 0

# (list) Permissions - 삼성 스토어에 필요한 최소 권한만
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API - 삼성 스토어는 보통 minSdkVersion 21 이상 권장
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Accept SDK license
android.accept_sdk_license = True

# (str) Android arch - 삼성 기기 호환성을 위해 armeabi-v7a와 arm64-v8a 모두 포함
android.archs = armeabi-v7a,arm64-v8a

# (bool) Debug mode - 릴리스 빌드는 False
android.debug = False

# (bool) Enable AndroidX support
android.use_androidx = True

# Gradle dependencies
android.gradle_dependencies = 'androidx.core:core:1.7.0'

# APK 파일명 설정
android.filename = sannaeeum

# (str) Package format - apk로 설정
android.package_format = apk

# 키스토어 설정
android.keystore = %(source.dir)s/sannaeeum.keystore
android.keystore_password = $(KEYSTORE_PASSWORD)
android.keystore_alias = sannaeeum
android.key_password = $(KEY_PASSWORD)

# (bool) Release build
android.release = True

# (str) Build tools version
android.build_tools = 33.0.2

# (str) Bootstrap
android.bootstrap = sdl2

# 앱 버전 코드 (증가시켜야 업데이트 가능)
android.version_code = 1

# 앱 버전 이름
android.version_name = 1.0.0

# (list) Android manifests extra entries - 삼성 스토어 호환성
android.extra_manifest_xml = <uses-feature android:glEsVersion="0x00020000" android:required="true"/>

# (bool) If True, then app can be installed on external storage
android.install_location = auto

#
# Logging
#
log_level = 2
