# This value will also be used for folder name
project = "LineageOS"
# Name of the parent folder used when uploading
project_type = "ROMs"
# These next 2 values are needed for lunch (e.g. "lineage"_whyred-"userdebug")
lunch_prefix = "lineage"
lunch_suffix = "userdebug"
# Target to build (e.g. to build a ROM's OTA package, use "bacon" or "otapackage", for a recovery project, use "recoveryimage")
build_target = "bacon"
# Filename of the output. You can also use wildcards if the name isn't fixed
artifacts = "lineage-*.zip"
