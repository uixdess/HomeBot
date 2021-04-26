from homebot.modules.ci.projects.aosp.project import AOSPProject

class DerpFestProject(AOSPProject):
	name = "DerpFest"
	category = "ROMs"
	lunch_prefix = "derp"
	lunch_suffix = "userdebug"
	build_target = "derp"
	artifacts = "DerpFest-11-*.zip"
