"""AOSP building CI module."""

from datetime import datetime
from homebot.modules.ci.project import ProjectBase
from homebot import bot_path, get_config
from homebot.modules.ci.parser import CIParser
from homebot.modules.ci.artifacts import Artifacts, STATUS_UPLOADING, STATUS_UPLOADED, STATUS_NOT_UPLOADED
from homebot.modules.ci.projects.aosp.post import PostManager
from homebot.modules.ci.projects.aosp.project import AOSPProject
from homebot.modules.ci.projects.aosp.returncode import SUCCESS, ERROR_CODES, NEEDS_LOGS_UPLOAD
from homebot.modules.ci.upload import Uploader
from importlib import import_module
from pathlib import Path
import re
import subprocess
from telegram.ext import CallbackContext
from telegram.update import Update

class Project(ProjectBase):
	name = "AOSP"

	def __init__(self, update: Update, context: CallbackContext, args: list[str]):
		super().__init__(update, context, args)
		parser = CIParser(prog="/ci aosp")
		parser.set_output(self.update.message.reply_text)
		parser.add_argument('project', help='AOSP project')
		parser.add_argument('device', help='device codename')
		parser.add_argument('-ic', '--installclean', help='make installclean before building', action='store_true')
		parser.add_argument('-c', '--clean', help='make clean before building', action='store_true')
		parser.set_defaults(clean=False, installclean=False)
		self.parsed_args = parser.parse_args(args)

	def build(self):
		# Import project
		project: AOSPProject
		project = import_module(f"homebot.modules.ci.projects.aosp.projects.{self.parsed_args.project}", package="*").project

		project_dir = Path(f"{get_config('CI_MAIN_DIR')}/{project.name}-{project.version}")
		device_out_dir = project_dir / "out" / "target" / "product" / self.parsed_args.device

		artifacts = Artifacts(device_out_dir, project.artifacts)
		post_manager = PostManager(self.context, project, self.parsed_args.device, artifacts)

		if self.parsed_args.clean is True:
			clean_type = "clean"
		elif self.parsed_args.installclean is True:
			clean_type = "installclean"
		else:
			clean_type = "none"

		post_manager.update("Building")

		command = [bot_path / "modules" / "ci" / "projects" / "aosp" / "tools" / "building.sh",
				"--sources", project_dir,
				"--lunch_prefix", project.lunch_prefix,
				"--lunch_suffix", project.lunch_suffix,
				"--build_target", project.build_target,
				"--clean", clean_type,
				"--device", self.parsed_args.device]

		last_edit = datetime.now()
		process = subprocess.Popen(command, encoding="UTF-8",
								stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		while True:
			output = process.stdout.readline()
			if output == '' and process.poll() is not None:
				break
			if not output:
				continue

			now = datetime.now()
			if (now - last_edit).seconds < 300:
				continue

			result = re.search(r"\[ +([0-9]+% [0-9]+/[0-9]+)\]", output.strip())
			if result is None:
				continue
			result_split = str(result.group(1)).split()
			if len(result_split) != 2:
				continue

			percentage, targets = re.split(" +", result.group(1))
			post_manager.update(f"Building: {percentage} ({targets})")

			last_edit = now

		returncode = process.poll()

		# Process return code
		build_result = ERROR_CODES.get(returncode, "Build failed: Unknown error")

		post_manager.update(build_result)

		needs_logs_upload = NEEDS_LOGS_UPLOAD.get(returncode, False)
		if needs_logs_upload != False:
			log_file = open(project_dir / needs_logs_upload, "rb")
			self.context.bot.send_document(get_config("CI_CHANNEL_ID"), log_file)
			log_file.close()

		if returncode != SUCCESS or get_config("CI_UPLOAD_ARTIFACTS") != "true":
			return

		# Upload artifacts
		try:
			uploader = Uploader()
		except Exception as e:
			post_manager.update(f"{build_result}\n"
								f"Upload failed: {type(e)}: {e}")
			return

		artifacts.update()

		post_manager.update(build_result)

		for artifact in artifacts.artifacts:
			artifact.status = STATUS_UPLOADING
			post_manager.update(build_result)

			try:
				uploader.upload(artifact, Path(project.category) / self.parsed_args.device / project.name / project.android_version)
			except Exception as e:
				artifact.status = f"{STATUS_NOT_UPLOADED}: {type(e)}: {e}"
			else:
				artifact.status = STATUS_UPLOADED

			post_manager.update(build_result)
