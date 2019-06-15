from obs.ObsClient import ObsClient
from twitch.TwitchBot import TwitchBot
import json
import logging
import logging.config

class MockTwitchBot():
	def __init__(self, obs_config, twitch_config):
		self.log = logging.getLogger(__name__)
		self.obs_config = obs_config
		self.twitch_config = twitch_config
		self.obs_client = ObsClient(obs_config, self)

	def twitch_say(self, message):
		self.log.debug("Twitch Bot: recieved say '{}'".format(message))

	def twitch_done(self):
		self.log.debug("Twitch Bot: received 'Done'")

	def twitch_failed(self):
		self.log.debug("Twitch Bot: received 'Failed'")

	def twitch_sleep(self, duration):
		self.log.debug("Twitch Bot: received sleep for {} seconds".format(duration))

	def twitch_shutdown(self):
		self.log.debug("Twitch Bot: received 'Shutdown'")

	def start(self):
		self.log.debug("Twitch Bot: received 'Start'")

	def run_forever(self):
		self.log.debug("Twitch Bot: received 'run forever (Linux)'")

	def run_forever_win(self):
		self.log.debug("Twitch Bot: received 'run forever (Windows)'")

def main():

	broadcaster = {
		"name": "TinaTiel",
		"follower": False,
		"subscriber": False,
		"subscriber_duration": None,
		"moderator": False,
		"broadcaster": True
	}

	user1 = {
		"name": "Mr. Spams",
		"follower": True,
		"subscriber": False,
		"subscriber_duration": None,
		"moderator": False,
		"broadcaster": False
	}

	user2 = {
		"name": "Bob",
		"follower": True,
		"subscriber": False,
		"subscriber_duration": None,
		"moderator": False,
		"broadcaster": False
	}

	user3 = {
		"name": "Molly",
		"follower": True,
		"subscriber": False,
		"subscriber_duration": None,
		"moderator": False,
		"broadcaster": False
	}

	user4 = {
		"name": "Chase",
		"follower": True,
		"subscriber": False,
		"subscriber_duration": None,
		"moderator": False,
		"broadcaster": False
	}

	user5 = {
		"name": "Kathy",
		"follower": True,
		"subscriber": False,
		"subscriber_duration": None,
		"moderator": False,
		"broadcaster": False
	}

	# Set logging and get configuration information
	logging.basicConfig(level=logging.DEBUG)
	log = logging.getLogger(__name__)

	with open('config.json', encoding='utf-8') as json_file:
		try:
			data = json.load(json_file)
		except Exception as e:
			log.error("Cannot read config.json! Error message: \n" + str(e))
			return

	twitch_config = data.get('twitch', None)
	if(twitch_config is None):
		log.error("Cannot initialize, missing twitch configuration information!")
		return

	obs_config = data.get('obs', None)
	if(obs_config is None):
		log.error("Cannot initialize, missing obs configuration information!")
		return

	# Initiate connection and call the commands
	testbot = MockTwitchBot(obs_config, twitch_config)
	testbot.start()
	testbot.run_forever_win()

	testbot.obs_client.execute(broadcaster, 'birb')
	testbot.obs_client.execute(broadcaster, 'tiel') #alias for birb

	testbot.obs_client.disconnect()

# Run main code if this module is executed from the command line.
if __name__ == "__main__":
		main()