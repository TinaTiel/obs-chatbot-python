from obs.ObsClient import ObsClient
from twitch.TwitchBot import TwitchBot
import json
import logging
import logging.config

class ObsCommandBot(TwitchBot):
		def __init__(self, obs_config, twitch_config):
				super().__init__(**twitch_config)
				self.log = logging.getLogger(__name__)
				self.obs_client = ObsClient(obs_config, self)
				self.broadcaster = self.channel.split("#", 1)[1]

		def on_twitch_command(self, cmd):
				
				if(self.log.getEffectiveLevel() == logging.DEBUG):
					self._pretty_log_dict(cmd)

				if cmd['action'] == "obsstatus":
					if cmd['user']['broadcaster'] == True:
						self._report_status(cmd)

				if cmd['action'] in ['reset', 'reconnect', 'recover']:
					if cmd['user']['broadcaster'] == True:
						self.twitch_say("Attempting to reconnect to OBS...")
						if(self.obs_client.reconnect()):
							self._report_status(cmd)
						else:
							self.twitch_say("Could not recover @{}, ensure OBS Websockets is available and restart the bot.".format(self.broadcaster))

				# Finally just execute the command specified against the OBS client
				else:
						self.obs_client.execute(cmd["user"], cmd["action"])

		def _report_status(self, cmd):
			obs_status = self.obs_client.getVersion()
			if "Exception" in obs_status:
				obs_message = obs_status
			else:
				obs_message = "Connected to OBS Websockets version {}.".format(obs_status)

			self.twitch_say("Twitch Bot is up and running. {}".format(
				obs_message
			))
			self.twitch_failed()

		def _pretty_log_dict(self, d, depth = 0):
			self.log.debug("-----------------")
			self.log.debug("Received command:")
			for k,v in d.items():
				if isinstance(v, dict):
						self.log.debug("%s:" % k)
						self._pretty_log_dict(v, depth + 1)
				else:
						self.log.debug(("		" * depth) +
									"%s: %s" % (k,v))

def main():
	# Set logging and get configuration information

	with open('config.json', encoding='utf-8') as json_file:
		try:
			data = json.load(json_file)
		except Exception as e:
			print("Cannot read config.json! Error message: \n" + str(e))
			return

	log_level = getattr(logging, data.get('log_level', "INFO"))
	#logging.basicConfig(level=log_level, filename="bot.log")
	logging.basicConfig(level=log_level)

	log = logging.getLogger(__name__)
	logging.getLogger("obswebsocket").setLevel(logging.ERROR) # OBS websocket Core is spammy

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
	bot.run_forever()

# Run main code if this module is executed from the command line.
if __name__ == "__main__":
		main()