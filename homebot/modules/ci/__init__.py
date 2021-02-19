"""HomeBot CI module."""

from homebot import bot_path, get_config
from homebot.core.admin import user_is_admin
from homebot.core.logging import LOGE, LOGI
from homebot.modules.ci.parser import CIParser
from importlib import import_module
import os.path

def ci(update, context):
	if not user_is_admin(update.message.from_user.id):
		update.message.reply_text("Error: You are not authorized to use CI function of this bot.\n"
								  "Ask to who host this bot to add you to the authorized people list")
		return

	if get_config("CI_CHANNEL_ID") == "":
		update.message.reply_text("Error: CI channel or user ID not defined")
		LOGE("CI channel or user ID not defined")
		return

	parser = CIParser(prog="/ci")
	parser.set_output(update.message.reply_text)
	parser.add_argument('project', help='CI project')

	args_passed = update.message.text[len("/ci"):].split()
	args = parser.parse_args(args_passed)

	if not os.path.isfile(bot_path / "modules" / "ci" / "projects" / (args.project + ".py")):
		update.message.reply_text("Error: Project script not found")
		return

	project_module = import_module('homebot.modules.ci.projects.' + args.project, package="*")

	LOGI("CI workflow started, project: " + args.project)
	project_module.ci_build(update, context)
	LOGI("CI workflow finished, project: " + args.project)

commands = [
	[ci, ["ci"]]
]
