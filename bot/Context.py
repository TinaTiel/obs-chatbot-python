import bot
import os
from pathlib import Path
import logging
import logging.config
import json

# Configure Logging
#log_level = getattr(logging, data.get('log_level', "INFO"))
log_level = logging.DEBUG
logging.basicConfig(level=log_level)
logging.getLogger("obswebsocket").setLevel(logging.ERROR) # OBS websocket Core is spammy

log = logging.getLogger(__name__)
log.info("Initializing clients...")

# Define the various file roots
proj_root = Path(os.path.dirname(bot.__file__))
conf_root = Path(proj_root, '..', 'config')
secrets_root = Path(conf_root, 'secrets')

secrets_obs_file = Path(secrets_root, 'obs.json')
conf_commands_file = Path(conf_root, 'commands.json')

# Init the OBS Client
with open(secrets_obs_file, encoding='utf-8') as file:
	try:
		secrets_obs = json.load(file)
	except Exception as e:
		raise Exception("Cannot read obs secrets file({})! Error message: {}".format(os.path.abspath(file)), str(e))

obs_client = bot.ObsClient(secrets_obs.get('host'), secrets_obs.get('port'), secrets_obs.get('password'))
obs_client.connect()

# Init the Command Client
with open(conf_commands_file, encoding='utf-8') as file:
	try:
		conf_commands = json.load(file)
	except Exception as e:
		raise Exception("Cannot read commands config file({})! Error message: {}".format(os.path.abspath(file)), str(e))

command_client = bot.CommandClient()
command_client.load_commands(conf_commands)