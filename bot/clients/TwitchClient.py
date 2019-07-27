from bot.clients.twitch.TwitchBot import TwitchBot
import logging

class TwitchClient(TwitchBot):
		def __init__(self, twitch_config, command_client):
				super().__init__(**twitch_config)
				self.command_client = command_client
				self.broadcaster = self.channel.split("#", 1)[1]

		def on_twitch_command(self, cmd):
				
				if(self.log.getEffectiveLevel() == logging.DEBUG):
					self._pretty_log_dict(cmd)

				if cmd['action'] == "twitchstatus":
					self.twitch_say("bleedPurple Twitch Bot is up and running!")

				else:
					if(self.command_client is None):
						self.log.warn("Twitch Bot not connected to a command client!")
						self.twitch_failed()
					else:
						self.command_client.execute(cmd["user"], cmd["action"], cmd["args"])

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