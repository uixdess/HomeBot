from homebot import get_config
from homebot.logging import LOGE, LOGI, LOGD, LOGW

# Project-specific imports
import argparse
from homebot import bot_path
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

def make_ci_post(project_module, device, status, additional_info):
	text = "🛠 CI | {} ({})\n".format(project_module.name, project_module.android_version)
	text += "Device: {}\n".format(device)
	text += "Lunch flavor: {}_{}-{}\n".format(project_module.lunch_prefix, device, project_module.lunch_suffix)
	text += "\n"
	text += "Status: {}\n".format(status)
	text += "\n"
	if additional_info is not None:
		text += additional_info
	return text

def ci_build(update, context):
	project = update.message.text.split()[2]
	project_module = import_module('homebot.modules.ci_projects.aosp.projects.' + project, package="*")
	parser = argparse.ArgumentParser()
	parser.add_argument('project', help='AOSP project')
	parser.add_argument('-d', '--device', help='device codename')
	parser.add_argument('-ic', '--installclean', help='make installclean before building', action='store_true')
	parser.add_argument('-c', '--clean', help='make clean before building', action='store_true')
	parser.set_defaults(clean=False, installclean=False)
	args = parser.parse_args(update.message.text.split(' ', 2)[2].split())

	if args.clean is True:
		clean_type = "clean"
	elif args.installclean is True:
		clean_type = "installclean"
	else:
		clean_type = "none"

	message_id = context.bot.send_message(get_config("CI_CHANNEL_ID"),
								  make_ci_post(project_module, args.device, "Building", None)).message_id
	process = Popen([bot_path / "modules" / "ci_projects" / "aosp" / "tools" / "building.sh",
							"--project", project_module.project,
							"--name", project_module.name,
							"--android_version", project_module.android_version,
							"--lunch_prefix", project_module.lunch_prefix,
							"--lunch_suffix", project_module.lunch_suffix,
							"--build_target", project_module.build_target,
							"--artifacts", project_module.artifacts,
							"--device", args.device,
							"--main_dir", get_config("CI_MAIN_DIR"),
							"--clean", clean_type],
							stdout=PIPE, stderr=PIPE, universal_newlines=True)
	_, _ = process.communicate()
	
	context.bot.edit_message_text(chat_id=get_config("CI_CHANNEL_ID"), message_id=message_id,
								  text=make_ci_post(project_module, args.device,
													error_code.get(process.returncode, "Build failed: Unknown error"), None))

	if needs_logs_upload.get(process.returncode, False) != False:
		log_file = open(Path(get_config("CI_MAIN_DIR")) / project_module.project / needs_logs_upload.get(process.returncode), "rb")
		context.bot.send_document(get_config("CI_CHANNEL_ID"),
									log_file)
		log_file.close()
