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

# (list) Application requirements - 중요: 필수 패키지 추가
requirements = python3,kivy==2.2.1,pyjnius,android

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
android.api = 33

# (int) Minimum API
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Automatically accept SDK license
android.accept_sdk_license = True

# (str) Android architectures
android.archs = armeabi-v7a

# (bool) Debug mode (False for release)
android.debug = False

# (bool) Enable AndroidX support - 중요: 활성화
android.use_androidx = True

# (str) Gradle dependencies - 중요: AndroidX 추가
android.gradle_dependencies = 'androidx.core:core:1.9.0'

# (str) Gradle options
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
android.build_tools = 33.0.2

# (str) NDK version
android.ndk_version = 25.1.8937393

# (str) Bootstrap
android.bootstrap = sdl2

# (str) Log level
log_level = 2

[buildozer]

# (int) Log level
log_level = 2

# (bool) Warn if built as root
warn_on_root = 1
