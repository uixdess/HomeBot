from homebot import get_config
from homebot.logging import LOGE, LOGI, LOGD, LOGW

# Module-specific imports
from contextlib import redirect_stdout
from cowsay import *
import io

def cowsay(update, context):
	with io.StringIO() as buf, redirect_stdout(buf):
		try:
			cow(update.message.text.split(' ', 1)[1])
		except IndexError:
			update.message.reply_text("Error: Write something after the command!")
		else:
			update.message.reply_text("`{}`".format(buf.getvalue()), parse_mode="Markdown")

commands = [
	[cowsay, ['cowsay']]
]
