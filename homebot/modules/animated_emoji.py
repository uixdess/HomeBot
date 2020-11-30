from homebot import get_config
from homebot.logging import LOGE, LOGI, LOGD, LOGW
from homebot.modules_manager import register

from telegram.dice import Dice

@register(commands=['basket'])
def basket(update, context):
	update.message.reply_dice(emoji=Dice.BASKETBALL)

@register(commands=['dart'])
def dart(update, context):
	update.message.reply_dice(emoji=Dice.DARTS)

@register(commands=['dice'])
def dice(update, context):
	update.message.reply_dice(emoji=Dice.DICE)

@register(commands=['football'])
def football(update, context):
	update.message.reply_dice(emoji=Dice.FOOTBALL)
