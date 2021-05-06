"""dotOS R CI project."""

from homebot.modules.ci.projects.aosp.project import AOSPProject

class dotOSProject(AOSPProject):
	name = "dotOS"
	category = "ROMs"
	lunch_prefix = "dot"
	lunch_suffix = "userdebug"
	build_target = "bacon"
	artifacts = "dotOS-*.zip"
