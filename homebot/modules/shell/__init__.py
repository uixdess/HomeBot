"""HomeBot shell module."""

from homebot import get_config
from homebot.core.admin import user_is_admin
from homebot.core.logging import LOGI
import subprocess

def shell(update, context):
	if not user_is_admin(update.message.from_user.id):
		update.message.reply_text("Error: You are not authorized to load modules")
		return

	if len(update.message.text.split(' ', 1)) < 2:
		update.message.reply_text("No command provided")
		return

	command = update.message.text.split(' ', 1)[1]
	process = subprocess.Popen(command.split(), shell=True, executable="/bin/bash",
							   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
							   universal_newlines=True)
	stdout, stderr = process.communicate()
	update.message.reply_text(f"Command: {command}\n"
							  f"Return code: {process.returncode}\n\n"
							  f"stdout:\n"
							  f"{stdout}\n"
							  f"stderr:\n"
							  f"{stderr}")

commands = [
	[shell, ['shell']]
]
