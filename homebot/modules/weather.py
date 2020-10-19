from homebot import get_config
from homebot.logging import LOGE, LOGI, LOGD
from homebot.modules_manager import register

# Module-specific imports
import requests

@register(commands=['weather'])
def weather(update, context):
	try:
		city = update.message.text.split(' ', 1)[1]
	except IndexError:
		update.message.reply_text("City not provided")
		return
	if get_config("WEATHER_API_KEY", None) == None:
		update.message.reply_text("OpenWeatherMap API key not specified\nAsk the bot hoster to configure it")
		LOGE("OpenWeatherMap API key not specified, get it at https://home.openweathermap.org/api_keys")
		return
	URL = "https://api.openweathermap.org/data/2.5/weather"
	parameters = {
		"appid": get_config("WEATHER_API_KEY", None),
		"q": city,
		"units": get_config("WEATHER_TEMP_UNIT", "metric"),
	}
	temp_unit = {
		"imperial": "F",
		"metric": "C"
	}
	wind_unit = {
		"imperial": "mph",
		"metric": "km/h"
	}
	temp_unit = temp_unit.get(get_config("WEATHER_TEMP_UNIT", None), "K")
	wind_unit = wind_unit.get(get_config("WEATHER_TEMP_UNIT", None), "km/h")
	response = requests.get(url=URL, params=parameters).json()
	if response["cod"] != 200:
		update.message.reply_text("Error: " + response["message"])
		return
	city_name = response["name"]
	city_country = response["sys"]["country"]
	city_lat = response["coord"]["lat"]
	city_lon = response["coord"]["lon"]
	weather_type = response["weather"][0]["main"]
	weather_type_description = response["weather"][0]["description"]
	temp = response["main"]["temp"]
	temp_min = response["main"]["temp_min"]
	temp_max = response["main"]["temp_max"]
	humidity = response["main"]["humidity"]
	wind_speed = response["wind"]["speed"]
	update.message.reply_text(
		"Current weather for {}, {} ({}, {}):\n" \
		"Weather: {} ({})\n" \
		"Temperature: {}{} (Min: {}{} Max: {}{})\n" \
		"Humidity: {}%\n" \
		"Wind: {}{}"
		.format(
			city_name, city_country, city_lat, city_lon,
			weather_type, weather_type_description,
			temp, temp_unit, temp_min, temp_unit, temp_max, temp_unit,
			humidity,
			wind_speed, wind_unit)
		)
