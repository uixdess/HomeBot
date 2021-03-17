"""HomeBot animated emoji module."""

from homebot.core.modules_manager import ModuleBase
from telegram.dice import Dice
from telegram.ext import CallbackContext
from telegram.update import Update

class Module(ModuleBase):
	name = "animated_emoji"
	description = "Send animated emojis with a single command"
	version = "1.0.0"

	def basket(self, update: Update, context: CallbackContext):
		update.message.reply_dice(emoji=Dice.BASKETBALL)

	def dart(self, update: Update, context: CallbackContext):
		update.message.reply_dice(emoji=Dice.DARTS)

	def dice(self, update: Update, context: CallbackContext):
		update.message.reply_dice(emoji=Dice.DICE)

	def football(self, update: Update, context: CallbackContext):
		update.message.reply_dice(emoji=Dice.FOOTBALL)

	def slotmachine(self, update: Update, context: CallbackContext):
		update.message.reply_dice(emoji=Dice.SLOT_MACHINE)

	commands = {
		basket: ['basket'],
		dart: ['dart'],
		dice: ['dice'],
		football: ['football'],
		slotmachine: ['slotmachine']
	}
