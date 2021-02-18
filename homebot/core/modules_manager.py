from importlib import import_module
from telegram.ext import CommandHandler
from types import FunctionType

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
