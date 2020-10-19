# This value will also be used for folder name
project = "LineageOS-17.1"
# Name to display on Telegram post
name = "LineageOS 17.1"
# Android version to display on Telegram post
android_version = "10"
# These next 2 values are needed for lunch (e.g. "lineage"_whyred-"userdebug")
lunch_prefix = "lineage"
lunch_suffix = "userdebug"
# Target to build (e.g. to build a ROM's OTA package, use "bacon" or "otapackage", for a recovery project, use "recoveryimage")
build_target = "bacon"
# Filename of the output. You can also use wildcards if the name isn't fixed
artifacts = "lineage-*.zip"
