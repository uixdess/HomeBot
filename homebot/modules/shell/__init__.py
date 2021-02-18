"""HomeBot shell module."""

from homebot import get_config
from homebot.core.logging import LOGI
import subprocess

def shell(update, context):
	if str(update.message.from_user.id) not in get_config("BOT_ADMIN_USER_IDS").split():
		update.message.reply_text("Error: You are not authorized to load modules")
		LOGI(f"Access denied to user {update.message.from_user.id}")
		return
	LOGI(f"Access granted to user {update.message.from_user.id}")

	if len(update.message.text.split(' ', 1)) < 2:
		update.message.reply_text("No command provided")
		return

	command = update.message.text.split(' ', 1)[1]
	process = subprocess.Popen(command.split(),
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
