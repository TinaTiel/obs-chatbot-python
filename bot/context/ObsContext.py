import bot
import os
from pathlib import Path
import json
import bot.context.AppContext as app
import logging


log = logging.getLogger(__name__)
log.info("Initializing OBS Context...")

# import inspect
# print(str(inspect.getmembers(app)))

secrets_obs_file = Path(app.secrets_root, 'obs.json')

# Init the OBS Client
with open(secrets_obs_file, encoding='utf-8') as file:
	try:
		secrets_obs = json.load(file)
	except Exception as e:
		raise Exception("Cannot read obs secrets file({})! Error message: {}".format(os.path.abspath(file)), str(e))

obs_client = bot.ObsClient(secrets_obs.get('host'), secrets_obs.get('port'), secrets_obs.get('password'))
obs_client.connect()

log.info("...Done.")