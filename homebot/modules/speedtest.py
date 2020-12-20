from homebot import get_config
from homebot.logging import LOGE, LOGI, LOGD, LOGW

# Module-specific imports
from speedtest import Speedtest

def speedtest(update, context):
	message_id = update.message.reply_text("Running speedtest...").message_id
	LOGI("Started")
	speedtest = Speedtest()
	speedtest.get_best_server()
	speedtest.download()
	speedtest.upload()
	speedtest.results.share()
	results_dict = speedtest.results.dict()
	download = str(results_dict["download"] // 10 ** 6)
	upload = str(results_dict["upload"] // 10 ** 6)
	context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=message_id,
								  text="Download: {} mbps\n"
									   "Upload: {} mbps".format(download, upload))
	LOGI("Finished, download: {} mbps, upload: {} mbps".format(download, upload))

commands = [
	[speedtest, ['speedtest']]
]
