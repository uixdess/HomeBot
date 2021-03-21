from homebot import __version__, get_config, modules
from homebot.core.bot import HomeBotUpdater
from homebot.core.logging import LOGI
from homebot.core.modules_manager import import_bot_modules

def main():
	global modules
	modules += import_bot_modules()
	updater = HomeBotUpdater(get_config("BOT_API_TOKEN"))
	LOGI(f"HomeBot started, version {__version__}")
	LOGI(f"Bot username: @{updater.bot.get_me().username}")
	updater.start_polling()
