from homebot import __version__, get_config
from homebot.core.bot import Bot
from homebot.core.logging import LOGI

def main():
	bot = Bot(get_config("BOT_API_TOKEN"))
	LOGI("HomeBot started, version " + str(__version__))
	LOGI("Bot username: @" + bot.updater.bot.get_me().username)
	bot.updater.start_polling()
