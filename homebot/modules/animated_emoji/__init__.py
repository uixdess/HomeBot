from telegram.dice import Dice

def basket(update, context):
	update.message.reply_dice(emoji=Dice.BASKETBALL)

def dart(update, context):
	update.message.reply_dice(emoji=Dice.DARTS)

def dice(update, context):
	update.message.reply_dice(emoji=Dice.DICE)

def football(update, context):
	update.message.reply_dice(emoji=Dice.FOOTBALL)

def slotmachine(update, context):
	update.message.reply_dice(emoji=Dice.SLOT_MACHINE)

commands = [
	[basket, ['basket']],
	[dart, ['dart']],
	[dice, ['dice']],
	[football, ['football']],
	[slotmachine, ['slotmachine']]
]
