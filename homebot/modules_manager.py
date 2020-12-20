from homebot import bot_path, dispatcher, get_config
from homebot.logging import LOGE, LOGI, LOGD, LOGW

from importlib import import_module
from pkgutil import iter_modules
from telegram.ext import CommandHandler
from types import FunctionType
from typing import List

modules_dir = bot_path / "modules"

modules = []

class Command:
	"""
	A class representing a HomeBot command
	"""
	def __init__(self, function: FunctionType, commands: list) -> None:
		self.function = function
		self.name = self.function.__name__
		self.commands = commands
		self.handler = CommandHandler(self.commands, self.function, run_async=True)

class Module:
	"""
	A class representing a HomeBot module
	"""
	def __init__(self, name: str) -> None:
		self.name = name
		self.module = import_module('homebot.modules.' + self.name, package="*")
		self.commands = [Command(command[0], command[1]) for command in self.module.commands]
		LOGI("Commands in module {}: {}".format(self.name, ", ".join([command.name for command in self.commands])))
		self.status = "Disabled"

	def load(self) -> None:
		LOGI("Loading module {}".format(self.name))
		self.status = "Starting up"
		for command in self.commands:
			try:
				dispatcher.add_handler(command.handler)
			except:
				LOGE("Error enabling module {}, command {}".format(self.name, command))
				self.status = "Error"
				raise
		else:
			LOGI("Module {} loaded".format(self.name))
			self.status = "Running"
	
	def unload(self) -> None:
		LOGI("Unloading module {}".format(self.name))
		self.status = "Starting up"
		for command in self.commands:
			try:
				dispatcher.remove_handler(command.handler)
			except:
				LOGE("Error disabling module {}, command {}".format(self.name, command))
				self.status = "Error"
				raise
		else:
			LOGI("Module {} unloaded".format(self.name))
			self.status = "Disabled"

def init_modules():
	global modules
	for module in [name for _, name, _ in iter_modules([modules_dir])]:
		module_class = Module(module)
		module_class.load()
		modules += [module_class]
	LOGI("Modules loaded")

def get_modules_list() -> List[Module]:
	return modules
