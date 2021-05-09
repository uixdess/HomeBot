from homebot.modules.ci.projects.aosp.project import AOSPProject

class crDroidProject(AOSPProject):
	name = "crDroid"
	category = "ROMs"
	lunch_prefix = "lineage"
	lunch_suffix = "userdebug"
	build_target = "bacon"
	artifacts = "crDroidAndroid-*.zip"
