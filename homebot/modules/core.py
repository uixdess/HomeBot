from homebot import get_config
from homebot.logging import LOGE, LOGI, LOGD, LOGW
from homebot.modules_manager import register

# Module-specific imports
from homebot import __version__
from homebot.modules_manager import get_modules_list

@register(commands=['start', 'help'])
def start(update, context):
	update.message.reply_text("Hi! I'm HomeBot, a bot written in Python by SebaUbuntu\n"
							  "Version {}\n"
							  "To see all the available modules, type /modules".format(__version__))

@register(commands=['modules'])
def modules(update, context):
	message = "Loaded modules:\n\n"
	for module in get_modules_list():
		message += "{}\n".format(module.name)
		message += "Status: {}\n".format(module.status)
		message += "Functions: {}\n\n".format(", ".join(module.functions))

	update.message.reply_text(message)
