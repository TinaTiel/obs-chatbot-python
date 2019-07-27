from bot.clients.CommandClient import CommandClient
import bot.context.AppContext as app
import os
from pathlib import Path
import json
import logging

log = logging.getLogger(__name__)
log.info("Initializing Command Context...")

conf_commands_file = Path(app.conf_root, 'commands.json')
# Init the Command Client
with open(conf_commands_file, encoding='utf-8') as file:
	try:
		conf_commands = json.load(file)
	except Exception as e:
		raise Exception("Cannot read commands config file({})! Error message: {}".format(os.path.abspath(file)), str(e))

command_client = CommandClient()
command_client.load_commands(conf_commands)

log.info("...Done.")