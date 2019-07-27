import bot
import bot.context.AppContext as app
import os
from pathlib import Path
import json
import logging


log = logging.getLogger(__name__)
log.info("Initializing Twitch Context...")

# import inspect
# print(str(inspect.getmembers(app)))

secrets_twitch_file = Path(app.secrets_root, 'twitch.json')

# Init the OBS Client
with open(secrets_twitch_file, encoding='utf-8') as file:
	try:
		secrets_twitch = json.load(file)
	except Exception as e:
		raise Exception("Cannot read Twitch secrets file({})! Error message: {}".format(os.path.abspath(file)), str(e))

twitch_client = bot.clients.TwitchClient(secrets_twitch, None)
twitch_client.start()
log.info("...Done. Verify with !twitchstatus, and press CTRL-C to exit when ready!\n")
twitch_client.run_forever()
