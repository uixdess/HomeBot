from homebot.modules.ci.projects.aosp.projects.projectfluid import common

# Android version to display on Telegram post
version = "11.0"
android_version = "11"

# This value will also be used for folder name
project = common.project
# Name of the parent folder used when uploading
project_type = common.project_type
# These next 2 values are needed for lunch (e.g. "lineage"_whyred-"userdebug")
lunch_prefix = common.lunch_prefix
lunch_suffix = common.lunch_suffix
# Target to build (e.g. to build a ROM's OTA package, use "bacon" or "otapackage", for a recovery project, use "recoveryimage")
build_target = common.build_target
# Filename of the output. You can also use wildcards if the name isn't fixed
artifacts = common.artifacts
