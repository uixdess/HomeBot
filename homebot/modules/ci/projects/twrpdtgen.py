from homebot import get_config
from homebot.core.logging import LOGE, LOGI, LOGD, LOGW
from telegram import Update
from telegram.ext import CallbackContext

# Project-specific imports
from github import Github, GithubException
from pathlib import Path
import requests
from tempfile import TemporaryDirectory
from twrpdtgen.device_tree import DeviceTree

def ci_build(update: Update, context: CallbackContext):
	update.message.reply_text("Generation started")
	tempdir = TemporaryDirectory()
	path = Path(tempdir.name)
	url = update.message.text.split()[2]
	file = path / "recovery.img"
	open(file, 'wb').write(requests.get(url, allow_redirects=True).content)

	try:
		devicetree = DeviceTree(path / "working", recovery_image=file)
	except Exception as e:
		update.message.reply_text("TWRP device tree generation failed\n"
								  f"Error: {e}")
		return

	# Upload to GitHub
	gh_username = get_config("CI_GITHUB_USERNAME")
	gh_token = get_config("CI_GITHUB_TOKEN")
	gh_org_name = get_config("CI_TWRPDTGEN_GITHUB_ORG")
	repo_name = "android_device_" + devicetree.manufacturer + "_" + devicetree.codename
	git_repo_url = f"https://{gh_username}:{gh_token}@github.com/{gh_org_name}/{repo_name}"

	try:
		gh = Github(gh_token)
		gh_org = gh.get_organization(gh_org_name)
		devicetree_repo = gh_org.create_repo(name=repo_name, private=False, auto_init=False)
		devicetree.git_repo.git.push(git_repo_url, "master")
	except GithubException as error:
		if error.status == 422:
			push_result = "Error: A device tree for this device already exists!"
		else:
			push_result = "Error: Push to GitHub failed!"
		update.message.reply_text(push_result)
	else:
		context.bot.send_message(get_config("CI_TWRPDTGEN_CHANNEL_ID"),
								  "TWRP device tree generated\n"
								 f"Codename: {devicetree.codename}\n"
								 f"Manufacturer: {devicetree.manufacturer}\n"
								 f"Device tree: {devicetree_repo.html_url}")
	finally:
		tempdir.cleanup()
