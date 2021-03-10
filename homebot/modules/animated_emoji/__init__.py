"""HomeBot animated emoji module."""

from telegram.dice import Dice
from telegram.ext import CallbackContext
from telegram.update import Update

def basket(update: Update, context: CallbackContext):
	update.message.reply_dice(emoji=Dice.BASKETBALL)

def dart(update: Update, context: CallbackContext):
	update.message.reply_dice(emoji=Dice.DARTS)

def dice(update: Update, context: CallbackContext):
	update.message.reply_dice(emoji=Dice.DICE)

def football(update: Update, context: CallbackContext):
	update.message.reply_dice(emoji=Dice.FOOTBALL)

def slotmachine(update: Update, context: CallbackContext):
	update.message.reply_dice(emoji=Dice.SLOT_MACHINE)

commands = [
	[basket, ['basket']],
	[dart, ['dart']],
	[dice, ['dice']],
	[football, ['football']],
	[slotmachine, ['slotmachine']]
]
