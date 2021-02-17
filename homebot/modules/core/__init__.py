from homebot import get_config
from homebot.logging import LOGE, LOGI, LOGD, LOGW

# Module-specific imports
from homebot import __version__
from homebot.core.bot import get_bot_context

def start(update, context):
	update.message.reply_text("Hi! I'm HomeBot, a bot written in Python by SebaUbuntu\n"
							  "Version {}\n"
							  "To see all the available modules, type /modules".format(__version__))

def modules(update, context):
	message = "Loaded modules:\n\n"
	modules = get_bot_context().modules
	for module in modules:
		message += "{}\n".format(module.name)
		message += "Status: {}\n".format(modules[module])
		message += "Commands: {}\n\n".format(", ".join([command.name for command in module.commands]))

	update.message.reply_text(message)

def load(update, context):
	if str(update.message.from_user.id) not in get_config("BOT_ADMIN_USER_IDS").split():
		update.message.reply_text("Error: You are not authorized to load modules")
		LOGI("Access denied to user " + str(update.message.from_user.id))
		return

	try:
		module_name = update.message.text.split(' ', 1)[1]
	except IndexError:
		update.message.reply_text("Error: Module name not provided")
		return

	if module_name == "core":
		update.message.reply_text("Error: You can't load module used for loading/unloading modules")
		return

	bot_context = get_bot_context()
	modules = bot_context.modules
	for module in modules:
		if module_name == module.name:
			bot_context.load_module(module)
			update.message.reply_text("Module {} loaded".format(module_name))
			return

	update.message.reply_text("Error: Module not found")

def unload(update, context):
	if str(update.message.from_user.id) not in get_config("BOT_ADMIN_USER_IDS").split():
		update.message.reply_text("Error: You are not authorized to unload modules")
		LOGI("Access denied to user " + str(update.message.from_user.id))
		return

	try:
		module_name = update.message.text.split(' ', 1)[1]
	except IndexError:
		update.message.reply_text("Error: Module name not provided")
		return

	if module_name == "core":
		update.message.reply_text("Error: You can't unload module used for loading/unloading modules")
		return

	bot_context = get_bot_context()
	modules = bot_context.modules
	for module in modules:
		if module_name == module.name:
			bot_context.unload_module(module)
			update.message.reply_text("Module {} unloaded".format(module_name))
			return

	update.message.reply_text("Error: Module not found")

commands = [
	[start, ['start', 'help']],
	[modules, ['modules']],
	[load, ['load']],
	[unload, ['unload']]
]
