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

user1 = {
	"name": "Mr. Spams",
	"follower": True,
	"subscriber": False,
	"subscriber_duration": None,
	"moderator": False
}

user2 = {
	"name": "Bob",
	"follower": True,
	"subscriber": False,
	"subscriber_duration": None,
	"moderator": False
}

user3 = {
	"name": "Molly",
	"follower": True,
	"subscriber": False,
	"subscriber_duration": None,
	"moderator": False
}

user4 = {
	"name": "Chase",
	"follower": True,
	"subscriber": False,
	"subscriber_duration": None,
	"moderator": False
}

user5 = {
	"name": "Kathy",
	"follower": True,
	"subscriber": False,
	"subscriber_duration": None,
	"moderator": False
}

try:
	pass
	client.execute(user1, 'pride')
	client.execute(user1, 'trans') # alias to 'pride' command
	client.execute(user1, 'talktome')
	client.execute(user1, 'talktome') # spam; not unique name
	client.execute(user1, 'talktome') # spam; not unique name
	client.execute(user1, 'talktome') # spam; not unique name
	client.execute(user1, 'talktome') # spam; not unique name
	client.execute(user2, 'talktome')
	client.execute(user3, 'talktome')
	client.execute(user4, 'talktome')
	client.execute(user5, 'talktome') # now votes reset

	client.execute(user1, 'talktome')

	client.disconnect()
except:
	client.disconnect()
	raise