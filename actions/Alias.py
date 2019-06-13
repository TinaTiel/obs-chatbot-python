import logging
import Common
from Message import Message

class Alias:
	"""Simply allows an alias for another function, for example the main 
	command may be 'cat' but an alias may be 'kitty'
	"""

	def __init__(self, obs_client, command_name, permission, min_votes, args):
		"""Initializes this class
		
		Parameters:
		obs_client (ObsClient): Reference to parent object
		command_name (string): chat command associated with this class instance
		permission (Permission): Permission level associated with command TODO: Use this??
		args (object): Arguments for this class instance, such as scene name, duration, etc.

		"""
		self.log = logging.getLogger(__name__)
		self.obs_client = obs_client
		self.command_name = command_name
		self.permission = permission
		self.min_votes = votes
		self.votes = []
		self._init_args(args)

	def execute(self, user):
		# this command is just an alias, no permissions or votes to evaluate
		obs_client.execute(user, self.func_alias)

	def _init_args(self, args):
		"""This validates the arguments are valid for this instance, 
		and raises a ValueError if they aren't.

		args must contain:
		command_name (string): Name of the command this alias should execute.

		"""
		self.func_alias = args.get('command_name', None)
		if(self.func_alias is None):
			raise ValueError("Command {}: Args Error, missing 'command_name'".format(self.command_name))