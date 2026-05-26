[app]
title = Catering App
package.name = cateringapp
package.domain = org.kiramat
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,txt,json
version = 1.0
requirements = python3,kivy,pillow
orientation = portrait
fullscreen = 1
icon.filename = logo.png
presplash.filename = logo.png
android.permissions = INTERNET
android.api = 29
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.enable_androidx = True
log_level = 2
warn_on_root = 1
build_dir = .buildozer
bin_dir = ./bin

[buildozer]
log_level = 2
warn_on_root = 1