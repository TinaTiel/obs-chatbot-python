from ObsClient import ObsClient
import json
import logging
import logging.config

logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)

# Get the logger specified in the file

# Get the config data
with open('config.json', encoding='utf-8') as json_file:
	data = json.load(json_file)

# Initiate connection and call the commands
twitch_bot = "foo" # replace with reference to Devon's code
client = ObsClient(data, twitch_bot)

user = {
	"name": "somebody",
	"follower": True,
	"subscriber": False,
	"subscriber_duration": None,
	"moderator": False
}

try:
	pass
	#client.execute(user, 'pride')
	print(client.execute(user, 'trans'))
	#client.execute(user, 'talktome')
	client.disconnect()
except:
	client.disconnect()
	raise