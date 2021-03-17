"""HomeBot cowsay module."""

from contextlib import redirect_stdout
from cowsay import cow
from homebot.core.modules_manager import ModuleBase
import io
from telegram.ext import CallbackContext
from telegram.update import Update

class Module(ModuleBase):
	name = "cowsay"
	description = "Moo"
	version = "1.0.0"

	def cowsay(update: Update, context: CallbackContext):
		with io.StringIO() as buf, redirect_stdout(buf):
			try:
				cow(update.message.text.split(' ', 1)[1])
			except IndexError:
				update.message.reply_text("Error: Write something after the command!")
			else:
				update.message.reply_text(f"`{buf.getvalue()}`", parse_mode="Markdown")

	commands = {
		cowsay: ['cowsay']
	}
