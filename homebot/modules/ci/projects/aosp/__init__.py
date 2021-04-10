"""AOSP building CI module."""

from datetime import datetime
from homebot import bot_path, get_config
from homebot.modules.ci.parser import CIParser
from homebot.modules.ci.artifacts import Artifacts, STATUS_UPLOADING, STATUS_UPLOADED, STATUS_NOT_UPLOADED
from homebot.modules.ci.projects.aosp.post import update_ci_post
from homebot.modules.ci.projects.aosp.project import AOSPProject
from homebot.modules.ci.projects.aosp.returncode import SUCCESS, ERROR_CODES, NEEDS_LOGS_UPLOAD
from homebot.modules.ci.upload import Uploader
from importlib import import_module
from pathlib import Path
import re
import subprocess
from telegram.ext import CallbackContext
from telegram.update import Update

def ci_build(update: Update, context: CallbackContext):
	# Parse arguments
	parser = CIParser(prog="/ci aosp")
	parser.set_output(update.message.reply_text)
	parser.add_argument('project', help='AOSP project')
	parser.add_argument('device', help='device codename')
	parser.add_argument('-ic', '--installclean', help='make installclean before building', action='store_true')
	parser.add_argument('-c', '--clean', help='make clean before building', action='store_true')
	parser.set_defaults(clean=False, installclean=False)

	try:
		args_passed = update.message.text.split(' ', 2)[2].split()
	except IndexError:
		args_passed = []

	args = parser.parse_args(args_passed)

	# Import project
	project: AOSPProject
	project = import_module(f"homebot.modules.ci.projects.aosp.projects.{args.project}", package="*").project

	project_dir = Path(f"{get_config('CI_MAIN_DIR')}/{project.name}-{project.version}")
	device_out_dir = project_dir / "out" / "target" / "product" / args.device

	if args.clean is True:
		clean_type = "clean"
	elif args.installclean is True:
		clean_type = "installclean"
	else:
		clean_type = "none"

	message_id = update_ci_post(context, None, project, args.device, "Building")

	command = [bot_path / "modules" / "ci" / "projects" / "aosp" / "tools" / "building.sh",
			   "--sources", project_dir,
			   "--lunch_prefix", project.lunch_prefix,
			   "--lunch_suffix", project.lunch_suffix,
			   "--build_target", project.build_target,
			   "--clean", clean_type,
			   "--device", args.device]

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
		if (now - last_edit).seconds < 30:
			continue

		result = re.search(r"\[ +([0-9]+% [0-9]+/[0-9]+)\]", output.strip())
		if result is None:
			continue
		result_split = str(result.group(1)).split()
		if len(result_split) != 2:
			continue

		percentage, targets = re.split(" +", result.group(1))
		update_ci_post(context, message_id, project, args.device,
					   f"Building: {percentage} ({targets})")

		last_edit = now

	returncode = process.poll()

	# Process return code
	build_result = ERROR_CODES.get(returncode, "Build failed: Unknown error")

	update_ci_post(context, message_id, project, args.device, build_result)

	needs_logs_upload = NEEDS_LOGS_UPLOAD.get(returncode, False)
	if needs_logs_upload != False:
		log_file = open(project_dir / needs_logs_upload, "rb")
		context.bot.send_document(get_config("CI_CHANNEL_ID"), log_file)
		log_file.close()

	if returncode != SUCCESS or get_config("CI_UPLOAD_ARTIFACTS") != "true":
		return

	# Upload artifacts
	try:
		uploader = Uploader()
	except Exception as e:
		update_ci_post(context, message_id, project, args.device,
					   f"{build_result}\n"
					   f"Upload failed: {type(e)}: {e}")
		return

	artifacts = Artifacts(device_out_dir, project.artifacts)

	update_ci_post(context, message_id, project, args.device, build_result, artifacts=artifacts)

	for artifact in artifacts.artifacts:
		artifact.status = STATUS_UPLOADING
		update_ci_post(context, message_id, project, args.device, build_result, artifacts=artifacts)

		try:
			uploader.upload(artifact, Path(project.category) / args.device / project.name / project.android_version)
		except Exception as e:
			artifact.status = f"{STATUS_NOT_UPLOADED}: {type(e)}: {e}"
		else:
			artifact.status = STATUS_UPLOADED

		update_ci_post(context, message_id, project, args.device, build_result, artifacts=artifacts)
