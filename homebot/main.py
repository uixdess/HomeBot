from homebot import __version__, get_config, modules
from homebot.core.bot import HomeBot
from homebot.core.logging import LOGI
from homebot.core.modules_manager import import_bot_modules

def main():
	global modules
	modules += import_bot_modules()
	bot = HomeBot(get_config("BOT_API_TOKEN"))
	LOGI(f"HomeBot started, version {__version__}")
	LOGI(f"Bot username: @{bot.updater.bot.get_me().username}")
	bot.updater.start_polling()
