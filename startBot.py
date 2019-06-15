from obs.ObsClient import ObsClient
from twitch.TwitchBot import TwitchBot
import json
import logging
import logging.config

def pretty_print_dict(d, depth = 0):
		for k,v in d.items():
				if isinstance(v, dict):
						print("%s:" % k)
						pretty_print_dict(v, depth + 1)
				else:
						print(("		" * depth) +
									"%s: %s" % (k,v))

class ObsCommandBot(TwitchBot):
		def __init__(self, obs_config, twitch_config):
				super().__init__(**twitch_config)
				self.log = logging.getLogger(__name__)
				self.obs_client = ObsClient(obs_config, self)

		def on_twitch_command(self, cmd):
				print("-----------------")
				print("Received command:")
				pretty_print_dict(cmd)

				if cmd["action"] == "say":
						if cmd["args"]:
								self.twitch_say(cmd["args"])
						else:
								self.twitch_say("What do you want me to say?")
				else:
						self.obs_client.execute(cmd["user"], cmd["action"])
				self.twitch_failed() # Always "fail" so cooldown timer is not used.

def main():
	# Set logging and get configuration information
	logging.basicConfig(level=logging.DEBUG)
	log = logging.getLogger(__name__)

	with open('config.json', encoding='utf-8') as json_file:
		data = json.load(json_file)

	twitch_config = data.get('twitch', None)
	if(twitch_config is None):
		log.error("Cannot initialize, missing twitch configuration information!")
		return

	obs_config = data.get('obs', None)
	if(obs_config is None):
		log.error("Cannot initialize, missing obs configuration information!")
		return
	# Initiate connection and call the commands
	bot = ObsCommandBot(obs_config, twitch_config)
	bot.start()
	bot.run_forever_win()
	#bot.run_forever()

# Run main code if this module is executed from the command line.
if __name__ == "__main__":
		main()