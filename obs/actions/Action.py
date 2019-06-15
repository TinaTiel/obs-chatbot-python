import obswebsocket, obswebsocket.requests
import logging
import time
from obs.Permission import Permission

class Action:

	def __init__(self, obs_client, command_name, aliases, description, permission, min_votes, args):
		"""Initializes this class
		
		Parameters:
		obs_client (ObsClient): Reference to parent object
		command_name (string): chat command associated with this class instance
		description (string): description of the chat command
		permission (Permission): Permission level associated with command
		min_votes (string): minimimum votes required for the command to execute
		args (object): Arguments for this class instance, such as scene name, duration, etc.
		"""

		self.log = logging.getLogger(__name__)
		self.obs_client = obs_client
		self.command_name = command_name
		self.aliases = aliases
		self.description = description
		self.permission = permission
		self.min_votes = min_votes
		self.votes = set()

	def execute(self, user):
		raise NotImplementedError("The action isn't defined!")

	def _init_args(self, args):
		raise NotImplementedError("The action isn't defined!")

	def _has_enough_votes(self, user):
		self.votes.add(user['name'])
		votes_received = len(self.votes)
		if(not votes_received >= self.min_votes):
			self.log.debug("Command {}: Insufficient votes, {} received of {} required.".format(self.command_name, votes_received, self.min_votes))
			remaining_votes = self.min_votes - votes_received
			self._twitch_say("{} votes to {} Will {} more join them? (!{})".format(user['name'], self.description, remaining_votes, self.command_name))
			return False
		else:
			self.votes = set()
			self.log.debug("Command {}: All votes received".format(self.command_name))
			return True

	def _has_permission(self, user):
		"""Gets the permission level of a given user and 
		checks if their permission is at least the required permission. 
		See the Permission class; MODERATOR > SUBSCRIBER > FOLLOWER > EVERYONE
		"""
		# First determine the user's permision level
		if(user['broadcaster']):
			user_permission = Permission.BROADCASTER
		elif(user['moderator']):
			user_permission = Permission.MODERATOR
		elif(user['subscriber']):
			user_permission = Permission.SUBSCRIBER
		elif(user['follower']):
			user_permission = Permission.FOLLOWER
		else:
			user_permission = Permission.EVERYONE
		
		result = user_permission >= self.permission
		self.log.debug("User '{}' has permission {} and required permission is {}. Operation Allowed: {}".format(user['name'], user_permission, self.permission, result))

		return result

	def _twitch_say(self, message):
		self.obs_client.twitch_bot.twitch_say(message)

	def _twitch_done(self):
		self.obs_client.twitch_bot.twitch_done()

	def _twitch_failed(self):
		self.obs_client.twitch_bot.twitch_failed()

	def _twitch_sleep(self, duration):
		self.obs_client.twitch_bot.twitch_sleep()

	def _twitch_shutdown(self):
		self.obs_client.twitch_bot.twitch_shutdown()