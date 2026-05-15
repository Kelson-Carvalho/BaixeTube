[app]
title = BaixeTube
package.name = baixetube
package.domain = org.baixetube
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = screens/*.py,utils/*.py
version = 1.0
requirements = python3,kivy==2.2.1,requests,pillow,certifi,charset-normalizer,urllib3,idna,yt-dlp
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 26
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True
android.arch = arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
