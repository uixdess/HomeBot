"""AOSP building CI module."""

from homebot import bot_path, get_config
from homebot.modules.ci.parser import CIParser
from homebot.modules.ci.upload import upload
from importlib import import_module
from pathlib import Path
from subprocess import Popen, PIPE

error_code = {
	0: "Build completed successfully",
	4: "Build failed: Missing arguments or wrong building path",
	5: "Build failed: Lunching failed",
	6: "Build failed: Cleaning failed",
	7: "Build failed: Building failed"
}

needs_logs_upload = {
	5: "lunch_log.txt",
	6: "clean_log.txt",
	7: "build_log.txt"
}

def make_ci_post(project_module, device, status, additional_info) -> str:
	text =  f"🛠 CI | {project_module.project} {project_module.version} ({project_module.android_version})\n"
	text += f"Device: {device}\n"
	text += f"Lunch flavor: {project_module.lunch_prefix}_{device}-{project_module.lunch_suffix}\n"
	text += "\n"
	text += f"Status: {status}\n"
	text += "\n"
	if additional_info is not None:
		text += additional_info
	return text

def create_artifacts_list(artifacts):
	upload_method = get_config("CI_ARTIFACTS_UPLOAD_METHOD")
	artifact_total = len(artifacts)
	artifact_uploaded = 0
	for artifact in artifacts:
		artifact_uploaded += 1

	text =  f"Uploaded {artifact_uploaded} out of {artifact_total} artifact(s)\n"
	text += f"Upload method: {upload_method}\n\n"
	artifact_index = 1
	for artifact in artifacts:
		artifact_result = artifacts.get(artifact, "On queue")
		text += f"{artifact_index}) {artifact.name}: {artifact_result}\n"
		artifact_index = artifact_index + 1
	return text

def ci_build(update, context):
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
		args_passed = ""

	args = parser.parse_args(args_passed)

	project_module = import_module('homebot.modules.ci.projects.aosp.projects.' + args.project, package="*")

	projects_dir = Path(get_config("CI_MAIN_DIR"))
	project_dir = projects_dir / (project_module.project + "-" + project_module.version)
	out_dir = project_dir / "out"
	device_out_dir = out_dir / "target" / "product" / args.device

	if args.clean is True:
		clean_type = "clean"
	elif args.installclean is True:
		clean_type = "installclean"
	else:
		clean_type = "none"

	message_id = context.bot.send_message(get_config("CI_CHANNEL_ID"),
								  make_ci_post(project_module, args.device, "Building", None)).message_id
	process = Popen([bot_path / "modules" / "ci" / "projects" / "aosp" / "tools" / "building.sh",
							"--project", project_module.project + "-" + project_module.version,
							"--android_version", project_module.android_version,
							"--lunch_prefix", project_module.lunch_prefix,
							"--lunch_suffix", project_module.lunch_suffix,
							"--build_target", project_module.build_target,
							"--device", args.device,
							"--main_dir", get_config("CI_MAIN_DIR"),
							"--clean", clean_type],
							stdout=PIPE, stderr=PIPE, universal_newlines=True)
	_, _ = process.communicate()

	context.bot.edit_message_text(chat_id=get_config("CI_CHANNEL_ID"), message_id=message_id,
								  text=make_ci_post(project_module, args.device,
													error_code.get(process.returncode, "Build failed: Unknown error"), None))

	if needs_logs_upload.get(process.returncode, False) != False:
		log_file = open(project_dir / needs_logs_upload.get(process.returncode), "rb")
		context.bot.send_document(get_config("CI_CHANNEL_ID"), log_file)
		log_file.close()

	if get_config("CI_UPLOAD_ARTIFACTS") != "true":
		return

	build_result = error_code.get(process.returncode, "Build failed: Unknown error")

	artifacts = {artifact: "On queue" for artifact in list(device_out_dir.glob(project_module.artifacts))}

	context.bot.edit_message_text(chat_id=get_config("CI_CHANNEL_ID"), message_id=message_id,
								  text=make_ci_post(project_module, args.device, build_result,
													create_artifacts_list(artifacts)))

	for artifact in artifacts:
		artifacts[artifact] = "Uploading"
		context.bot.edit_message_text(chat_id=get_config("CI_CHANNEL_ID"), message_id=message_id,
									  text=make_ci_post(project_module, args.device, build_result,
														create_artifacts_list(artifacts)))

		result = upload(artifact, Path(project_module.project_type) / args.device / project_module.project / project_module.android_version)
		if result is True:
			artifacts[artifact] = "Upload successful"
		else:
			artifacts[artifact] = "Upload failed"

		context.bot.edit_message_text(chat_id=get_config("CI_CHANNEL_ID"), message_id=message_id,
									  text=make_ci_post(project_module, args.device, build_result,
														create_artifacts_list(artifacts)))
