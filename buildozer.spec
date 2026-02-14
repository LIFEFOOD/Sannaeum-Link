[app]
title = 산내음 링크
package.name = sannaeeumlink
package.domain = org.sannaeeum

source.dir = .
source.include_exts = py,png,jpg,kv,ttf

version = 0.1
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

requirements = python3,kivy,android

# 권한 설정
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# 아이콘 설정
icon.filename = %(source.dir)s/res/drawable/icon.png

# 폰트 파일 포함
source.include_patterns = res/fonts/*.ttf, res/drawable/*.png

# 안드로이드 API 레벨
android.api = 33
android.minapi = 21
android.sdk = 33

# 한글 지원을 위한 설정
android.accept_sdk_license = True

# 빌드 타겟
android.gradle_dependencies = 'com.android.support:support-annotations:28.0.0'

# 디버그 모드
android.debug = True

# 안드로이드 아키텍처
android.archs = armeabi-v7a, arm64-v8a

# 안드로이드 엔트리 포인트
android.entrypoint = org.kivy.android.PythonActivity

# 안드로이드 앱 이름
android.app_name = 산내음링크

# 안드로이드 앱 테마
android.theme = @android:style/Theme.DeviceDefault

# 안드로이드 방향 (가로/세로)
android.orientation = portrait

# 안드로이드 백업 허용
android.allow_backup = True

# 안드로이드 구글 플레이 서비스
android.play_services_version = 15.0.0

# 안드로이드 구글 라이선스 체크
android.licenses_check = True

[buildozer]
log_level = 2
warn_on_root = 1