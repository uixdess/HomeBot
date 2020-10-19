from homebot import get_config
from homebot.logging import LOGE, LOGI, LOGD
from homebot.modules_manager import register

# Module-specific imports
from homebot import __version__
from homebot.modules_manager import get_modules_list

@register(commands=['start', 'help'])
def start(update, context):
	update.message.reply_text("Hi! I'm HomeBot, a bot written in Python by SebaUbuntu\n" + \
							  "Version " + __version__ + "\n" + \
							  "To see all the available modules, type /modules")

@register(commands=['modules'])
def start(update, context):
	update.message.reply_text("Loaded modules:\n\n- " + \
							  '\n- '.join(get_modules_list()))
