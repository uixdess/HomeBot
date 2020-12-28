from homebot import get_config
from homebot.logging import LOGE, LOGI, LOGD, LOGW

# Module-specific imports
from homebot import bot_path
from ftplib import FTP, error_perm
from importlib import import_module
import os.path
import paramiko
from pathlib import Path
import shutil

def ftp_chdir(ftp, remote_directory):
	if remote_directory == '/':
		ftp.cwd('/')
		return
	if remote_directory == '':
		return
	try:
		ftp.cwd(remote_directory)
	except error_perm:
		dirname, basename = os.path.split(remote_directory.rstrip('/'))
		ftp_chdir(ftp, dirname)
		ftp.mkd(basename)
		ftp.cwd(basename)
		return True

def sftp_chdir(sftp, remote_directory):
	if remote_directory == '/':
		sftp.chdir('/')
		return
	if remote_directory == '':
		return
	try:
		sftp.chdir(remote_directory)
	except IOError:
		dirname, basename = os.path.split(remote_directory.rstrip('/'))
		sftp_chdir(sftp, dirname)
		sftp.mkdir(basename)
		sftp.chdir(basename)
		return True

def upload(file, destination_path_ci):
	method = get_config("CI_ARTIFACTS_UPLOAD_METHOD")
	destination_path_base = Path(get_config("CI_UPLOAD_BASE_DIR"))
	host = get_config("CI_UPLOAD_HOST")
	port = get_config("CI_UPLOAD_PORT")
	username = get_config("CI_UPLOAD_USERNAME")
	password = get_config("CI_UPLOAD_PASSWORD")

	ALLOWED_METHODS = ["localcopy", "ftp", "sftp"]
	file_path = Path(file)
	file_base = file_path.name

	if destination_path_base is None:
		destination_path = destination_path_ci
	else:
		destination_path = destination_path_base / destination_path_ci

	if method not in ALLOWED_METHODS:
		return "Upload method not valid"

	if not file_path.is_file():
		return "File doesn't exists"

	LOGI("Started uploading of", file)

	if method == "localcopy":
		os.makedirs(destination_path, exist_ok=True)
		shutil.copy(file_path, destination_path)

	elif method == "ftp":
		if port is None or port == "":
			server = host
		else:
			server = host + ":" + port
		ftp = FTP(server)
		ftp.login(username, password)
		ftp_chdir(ftp, destination_path)
		with open(file_path, 'rb') as f:
			ftp.storbinary('STOR %s' % file_base, f)
			f.close()
		ftp.close()

	elif method == "sftp":
		if port is None or port == "":
			server = host
		else:
			server = host + ":" + port
		transport = paramiko.Transport(server)
		transport.connect(username=username, password=password)
		sftp = paramiko.SFTPClient.from_transport(transport)

		sftp_chdir(sftp, destination_path)
		sftp.put(file_path, file_base)

		sftp.close()
		transport.close()

	LOGI("Finished uploading of", file)
	return True

def ci(update, context):
	if str(update.message.from_user.id) not in get_config("CI_APPROVED_USER_IDS").split():
		update.message.reply_text("Error: You are not authorized to use CI function of this bot.\nAsk to who host this bot to add you to the authorized people list")
		LOGI("Access denied to user " + str(update.message.from_user.id))
		return
	LOGI("Access granted to user " + str(update.message.from_user.id))
	if get_config("CI_CHANNEL_ID") == "":
		update.message.reply_text("Error: CI channel or user ID not defined")
		LOGE("CI channel or user ID not defined")
		return
	project = update.message.text.split()[1]
	if not os.path.isfile(bot_path / "modules" / "ci" / "projects" / (project + ".py")):
		update.message.reply_text("Error: Project script not found")
		return
	project_module = import_module('homebot.modules.ci.projects.' + project, package="*")
	LOGI("CI workflow started, project: " + project)
	project_module.ci_build(update, context)
	LOGI("CI workflow finished, project: " + project)

commands = [
	[ci, ["ci"]]
]
