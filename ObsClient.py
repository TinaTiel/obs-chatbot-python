# This class is responsible for making stuff happen in OBS
import obswebsocket, obswebsocket.requests
import logging
import time
from importlib import import_module
#from ActionShowSceneItem import ActionShowSceneItem
from Message import Message
from Permission import Permission

class ObsClient:
	"""This class is responsible for executing commands against OBS, given params
	from a configuration json file"""

	def __init__(self, conf, twitch_bot):
		self.log = logging.getLogger(__name__)
		self._load_config(conf)
		self._connect()
		self._init_commands()
		self.twitch_bot = twitch_bot

	def execute(self, user, command_name):
		"""Executes a given command with an user. The command is a string that is 
		used to refer to a function pointer, whose function is defined privately 
		in this class. For example a command_name 'foo' implies a method '_foo' in this 
		class
		"""
		self.log.debug("User '{}' trying to excecute command '{}'...".format(user['name'], command_name))

		# Verify if the command exists
		command = self.commands.get(command_name, None)
		if(command is None):
			self.log.warn("User error: '{}' tried to execute unknown or misconfigured command '{}'".format(user['name'], command_name))
			return

		# Execute the function with args, returning its message
		return command.execute(user)

	def disconnect(self):
		"""Disconnects the OBS client websocket. Should be called when 
		the process ends, NOT after every call
		"""
		self.client.disconnect()
		self.log.info("disconnected OBS Websocket _connection.")

	def _load_config(self, conf):
		"""Gets the configuration information from config.json and stores it
		to private variables
		"""
		self.log.info("Loading configuration fiel...")
		try:
			self.conf_obs = conf.get('obs_websockets', None)
			self.conf_commands = conf.get('commands', None)
			self.log.info("...Loaded configuration file.")
		except KeyError as e:
			self.log.error("Could not load config file, missing 'obs_websockets', or 'commands' elements!")
			raise

	def _init_commands(self):
		"""Initializes the commands as objects, so that they can have state and for
		example to keep an internal vote count
		"""
		self.commands = {}
		self.log.info("Initializing commands...")
		# Get all the commands and iterate over them
		for command in self.conf_commands:
			
			# Verify the necessary config elements exist at all
			name = command.get('name', "unknown")
			permission_str = command.get('permission', None)
			action = command.get('action', None)
			votes = command.get('votes', None)
			args = command.get('args', None)
			if(permission_str is None or action is None or votes is None or args is None):
				self.log.warn("Command '{}': Error, missing 'permission', 'action', 'votes', or 'args' elements for command ".format(name))
				continue

			# Verify the votes and permission string are valid
			if(votes < 0):
				self.log.warn("Command '{}': Error, votes cannot be less than zero for command {}".format(name, votes))
				continue
			else:
				self.log.debug("Command '{}': minimum votes is {}".format(name, votes))

			try:
				permission = Permission[permission_str]
				self.log.debug("Command '{}': permission is {}".format(name, permission))
			except Exception as e:
				self.log.warn("Command '{}': Error, permission string '{}' is invalid, must be one of: {}".format(name, permission_str, Permission.__members__))
				continue

			# Try to get the corresponding action class
			try:
				module = import_module("actions."+action)
				class_ = getattr(module, action)
				self.log.debug("Command {}: action is {}".format(name, class_))
			except Exception as e:
				self.log.warn("Command '{}': Error, no such action {} is defined. Full error: {}".format(name, action, e))
				continue

			# Try to instantiate the action class
			try:
				self.log.debug("Command {}: args are: {}".format(name, args))
				func = class_(self, name, permission, args) # TODO revisit the permissions thing in a class instance
			except ValueError:
				self.log.warn("Command '{}': Error, could not instantiate command class with args {}".format(name, args))
				continue

			# Add func to internal reference
			self.commands[name] = func

		self.log.info("...Commands initialized: {}".format(
				list( self.commands.keys()) 
			)
		)

	def _connect(self):
		"""Initiates connection with OBS Websockets, and will raise an exception 
		if it fails to connect for any reason whatsoever
		"""
		self.log.info("Trying to connect to OBS Websockets...")

		host = self.conf_obs.get('host')
		port = self.conf_obs.get('port')
		password = self.conf_obs.get('password')
		try:
				self.client = obswebsocket.obsws(host, port, password)
				self.client.connect()
				self.log.info("...Connected to OBS Websockets at {}:{}".format(host, port))
		except Exception as e:
			self.log.error("Could not initialize connection at {}:{} to OBS Websockets! Exception: {}".format(host, port, e))
			raise