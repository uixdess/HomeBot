from homebot import get_config
from homebot.logging import LOGE, LOGI, LOGD
from homebot.modules_manager import register

@register(commands=['basket'])
def basket(update, context):
	update.message.reply_dice(emoji="🏀")

@register(commands=['dart'])
def dart(update, context):
	update.message.reply_dice(emoji="🎯")

@register(commands=['dice'])
def dice(update, context):
	update.message.reply_dice(emoji="🎲")

@register(commands=['football'])
def football(update, context):
	update.message.reply_dice(emoji="⚽️")
