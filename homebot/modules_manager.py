from homebot import bot_path, dispatcher, get_config
from homebot.logging import LOGE, LOGI, LOGD, LOGW

from ast import parse as parse_module, FunctionDef
from importlib import import_module
from pkgutil import iter_modules
from telegram.ext import CommandHandler

modules_dir = bot_path / "modules"

modules = []
commands = []

class Module:
	"""
	A class representing a HomeBot module
	"""
	def __init__(self, name) -> None:
		self.name = name
		filename = modules_dir / (self.name + ".py")
		file_open = open(filename, "rt")
		tree = parse_module(file_open.read(), filename=filename)
		file_open.close()
		self.functions = [function.name for function in tree.body if isinstance(function, FunctionDef)]
		LOGI("Commands in module {}: {}".format(self.name, ", ".join(self.functions)))
		self.status = "Disabled"

	def load(self) -> None:
		LOGI("Loading module {}".format(self.name))
		self.status = "Starting up"
		try:
			self.module = import_module('homebot.modules.' + self.name, package="*")
		except:
			LOGE("Error importing module {}".format(self.name))
			self.status = "Error"
			raise
		else:
			LOGI("Module {} loaded".format(self.name))
			self.status = "Running"
	
	def unload(self) -> None:
		LOGI("Unloading {} is WIP".format(self.name))

def init_modules():
	global modules
	for module in [name for _, name, _ in iter_modules([modules_dir])]:
		module_class = Module(module)
		module_class.load()
		modules += [module_class]
	LOGI("Modules loaded")

def add_command(entry):
	global commands
	commands += entry

def remove_command(entry):
	global commands
	commands += entry

def get_modules_list():
	return modules

def get_commands_list():
	return commands

def register(commands):
	def decorator(func):
		async def wrapper(check):
			try:
				await func(check)
			except BaseException as e:
				LOGE(e)
			else:
				pass

		dispatcher.add_handler(CommandHandler(commands, func, run_async=True))

		if type(commands) is list:
			for command in commands:
				add_command(command)
		else:
			add_command(commands)

		return wrapper

	return decorator
