from homebot import __version__, get_config
from homebot.core.bot import Bot
from homebot.core.logging import LOGE, LOGI

def main():
	bot = Bot(get_config("BOT_API_TOKEN"))
	try:
		bot.updater.bot.get_me().username
	except:
		LOGE("Failed to connect to Telegram, check your internet connection and/or your bot token")
		exit()
	LOGI("HomeBot started, version " + str(__version__))
	LOGI("Bot username: @" + bot.updater.bot.get_me().username)
	bot.updater.start_polling()
