from homebot import modules
from homebot.core.error_handler import error_handler
from homebot.core.logging import LOGE, LOGI
from telegram.ext import Updater

class Bot:
	"""
	This class represent a bot instance.
	"""
	def __init__(self, token):
		"""
		Initialize the bot and its modules.
		"""
		LOGI("Initializing bot")
		self.updater = Updater(token=token, use_context=True)
		self.dispatcher = self.updater.dispatcher
		self.dispatcher.add_error_handler(error_handler, True)
		self.modules = []
		LOGI("Bot initialized")

		LOGI("Parsing modules")
		for module in modules:
			try:
				module_instance = module(self)
			except Exception as e:
				LOGE(f"Error initializing module {module.name}, will be skipped\n"
					 f"Error: {e}")
			else:
				self.modules.append(module_instance)
		LOGI("Modules parsed")

		LOGI("Loading modules")
		for module in self.modules:
			self.load_module(module)
		LOGI("Modules loaded")

	def load_module(self, module):
		"""
		Load a provided module and add its command handler
		to the bot's dispatcher.
		"""
		LOGI(f"Loading module {module.name}")
		module.set_status("Starting up")

		for command in module.commands:
			self.dispatcher.add_handler(command.handler)

		module.set_status("Running")
		LOGI(f"Module {module.name} loaded")

	def unload_module(self, module):
		"""
		Unload a provided module and remove its command handler
		from the bot's dispatcher.
		"""
		LOGI(f"Unloading module {module.name}")
		module.set_status("Stopping")

		for command in module.commands:
			self.dispatcher.remove_handler(command.handler)

		module.set_status("Disabled")
		LOGI(f"Module {module.name} unloaded")
