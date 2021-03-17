from homebot import modules_path
from homebot.core.bot import Bot
from homebot.core.logging import LOGE
from importlib import import_module
from pkgutil import iter_modules
from telegram.ext import CommandHandler
from types import FunctionType

def import_bot_modules():
	modules = []
	for module_name in [name for _, name, _ in iter_modules([modules_path])]:
		try:
			module_class = import_module(f'homebot.modules.{module_name}', package="Module").Module
		except Exception as e:
			LOGE(f"Error importing module {module_name}, will be skipped\n"
				 f"Error: {e}")
		else:
			modules.append(module_class)
	return modules

class Command:
	"""
	A class representing a HomeBot command
	"""
	def __init__(self, module, function: FunctionType, commands: list) -> None:
		"""
		Initialize the command class.
		"""
		self.name = function.__name__
		self.module = module
		self.commands = commands
		self.function = lambda update, context: function(self.module, update, context)
		self.handler = CommandHandler(self.commands, self.function, run_async=True)

class ModuleBase:
	"""
	A class representing a HomeBot module.
	This class must be used only as a superclass for all HomeBot modules.

	Subclasses must provide 4 variables:
	name: Name of the module.
	description: Description of the module.
	version: Version of the module.
	commands: A dictionary containing a function as the key
			  and a list of commands as the value.
	"""
	name: str
	description: str
	version: str
	commands: dict

	def __init__(self, bot: Bot) -> None:
		"""
		Initialize the module class and import its commands.
		"""
		if type(self) is ModuleBase:
			raise TypeError("You can't initialize a ModuleBase, it can only be used as a superclass")

		self.bot = bot
		self.status = "Disabled"
		self.commands = [Command(self, function, commands) for function, commands in self.commands.items()]

	def set_status(self, status: str) -> None:
		"""
		Change the status of the module.
		"""
		self.status = status
