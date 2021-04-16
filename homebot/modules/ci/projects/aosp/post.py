from homebot import get_config
from homebot.modules.ci.artifacts import Artifacts
from homebot.modules.ci.projects.aosp.project import AOSPProject
from telegram.error import TimedOut
from telegram.ext import CallbackContext

chat_id = get_config("CI_CHANNEL_ID")

class PostManager:
	def __init__(self, context: CallbackContext, project: AOSPProject, device: str, artifacts: Artifacts):
		self.context = context
		self.project = project
		self.device = device
		self.artifacts = artifacts
		self.base_message_text = self.get_base_message_text()
		self.message = self.context.bot.send_message(chat_id, self.base_message_text)

	def get_base_message_text(self):
		text =  f"🛠 CI | {self.project.name} {self.project.version} ({self.project.android_version})\n"
		text += f"Device: {self.device}\n"
		text += f"Lunch flavor: {self.project.lunch_prefix}_{self.device}-{self.project.lunch_suffix}\n"
		text += "\n"
		return text

	def update(self, status: str):
		text = self.base_message_text
		text += f"Status: {status}\n"
		text += "\n"
		if self.artifacts.artifacts:
			text += self.artifacts.get_readable_artifacts_list()
		self.edit_text(text)

	def edit_text(self, text):
		# FIXME:
		# telegram.vendor.ptb_urllib3.urllib3.exceptions.ReadTimeoutError:
		# HTTPSConnectionPool(host='api.telegram.org', port=443):
		# Read timed out. (read timeout=5.0)
		try:
			return self.message.edit_text(text)
		except TimedOut:
			pass
