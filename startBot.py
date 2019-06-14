from obs.ObsClient import ObsClient
import json
import logging
import logging.config

# Get the logger specified in the file
#logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
logging.basicConfig(level=logging.DEBUG)

# Get the config data
with open('config.json', encoding='utf-8') as json_file:
	data = json.load(json_file)

# Initiate connection and call the commands
twitch_bot = "foo" # replace with reference to Devon's code
client = ObsClient(data, twitch_bot)