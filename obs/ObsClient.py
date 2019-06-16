# This class is responsible for making stuff happen in OBS
import obswebsocket, obswebsocket.requests
import logging
import time
from importlib import import_module
from obs.Permission import Permission
from obs.actions.Help import Help

#TODO: Add duration to setScene, and for both SetScene and ShowSceneItem make it possible to have infinite duration / skip sleeping.
#TODO: set a value in a text file, for example an username so that it can be used in a scene as part of a chain displaying text and a gif
#TODO: Wait command
#TODO: Vote override if broadcaster or moderator

class ObsClient:
	"""This class is responsible for executing commands against OBS, given params
	from a configuration json file"""

	def __init__(self, conf, twitch_bot):
		self.log = logging.getLogger(__name__)
		self._load_config(conf)
		self._connect()
		self._init_commands()
		self.twitch_bot = twitch_bot
		self.max_attempts = 3 

	def execute(self, user, command_name):
		"""Executes a given command with an user. The command is a string corresponding
		to a class in the actions package, which is dynamically loaded if configured
		correctly.
		"""

		# Verify if the command exists
		command = self.commands.get(command_name, None)
		if(command is None):
			#self.log.warn("User error: '{}' tried to execute unknown or misconfigured command '{}'".format(user['name'], command_name))
			return self.twitch_bot.twitch_failed()

		# Execute the function with args, returning its message
		try:
			return command.execute(user) # Command class must call twitch_done() or twich_failed() on twitch_bot, it is not done here!
		except Exception as e:
			self.log.error("Could not execute command (Exception: {}), most likely an issue with the OBS connection. Trying to reconnect...".format(str(e)))
			if(not self.reconnect()):
				self.twitch_bot.twitch_say("Could not execute command !{} after {} attempts @{}! Ensure OBS Websockets is available and restart the bot".format(
					command_name,
					self.max_attempts,
					self.twitch_bot.channel.split("#", 1)[1]
				))
				self.twitch_bot.twitch_failed()
			else:
				return self.execute(user, command_name)

	def reconnect(self):
		try:
			self.disconnect()
		except:
			pass

		attempt = 0
		while attempt < self.max_attempts:
			self.log.warn("OBS reconnect attempt #{}".format(attempt+1))
			attempt += 1
			try:
				self._connect()
			except Exception as e:
				continue
			else:
				return True
		return False

	def disconnect(self):
		"""Disconnects the OBS client websocket. Should be called when 
		the process ends, NOT after every call
		"""
		self.client.disconnect()
		self.log.info("disconnected OBS Websocket _connection.")

	def getVersion(self):
		try:
			message = self.client.call(obswebsocket.requests.GetVersion()).getObsWebsocketVersion()
		except Exception as e:
			message = "Could not communicate with OBS. Exception: " + str(e)
		return message

	def _load_config(self, conf):
		"""Gets the configuration information from config.json and stores it
		to private variables
		"""
		self.log.info("Loading configuration file...")

		self.host = conf.get('host', None)
		self.port = conf.get('port', None)
		self.password = conf.get('password', None)
		self.conf_commands = conf.get('commands', None)

		if(   self.host is None
			 or self.port is None
			 or self.password is None
			 or self.conf_commands is None):
			raise KeyError("Could not initialize OBS Client, missing host, port, password, or conf_commands!")

		self.log.info("...Loaded configuration file.")

	def _init_commands(self):
		"""Initializes the commands as objects, so that they can have state and for
		example to keep an internal vote count
		"""
		self.commands = {}
		self.log.info("Initializing commands...")
		# Get all the commands and iterate over them
		for command in self.conf_commands:
			
			# Verify the necessary config elements exist at all
			command_name = command.get('name', "unknown")
			description = command.get('description', "")
			permission_str = command.get('permission', None)
			action = command.get('action', None)
			min_votes = command.get('min_votes', None)
			args = command.get('args', None)
			aliases = command.get('aliases', None)
			if(command_name is None 
				or permission_str is None 
				or action is None 
				or min_votes is None 
				or args is None):
				self.log.warn("Command '{}': Error, missing 'permission', 'action', 'min_votes', or 'args' elements for command ".format(command_name))
				continue

			# Verify the votes and permission string are valid
			if(min_votes < 0):
				self.log.warn("Command '{}': Error, min_votes cannot be less than zero for command {}".format(command_name, min_votes))
				continue
			else:
				self.log.debug("Command '{}': minimum votes is {}".format(command_name, min_votes))

			try:
				permission = Permission[permission_str]
				self.log.debug("Command '{}': permission is {}".format(command_name, permission))
			except Exception as e:
				self.log.warn("Command '{}': Error, permission string '{}' is invalid, must be one of: {}".format(command_name, permission_str, Permission.__members__))
				continue

			# Try to get the corresponding action class
			try:
				module = import_module("obs.actions."+action)
				class_ = getattr(module, action)
				self.log.debug("Command {}: action is {}".format(command_name, class_))
			except Exception as e:
				self.log.warn("Command '{}': Error, no such action {} is defined. Full error: {}".format(command_name, action, e))
				continue

			# Try to instantiate the action class
			try:
				self.log.debug("Command {}: args are: {}".format(command_name, args))
				command_obj = class_(self, command_name, aliases, description, permission, min_votes, args)
			except ValueError as e:
				self.log.warn(e)
				continue

			# Add command_obj to internal reference
			self.commands[command_name] = command_obj

			# If there are aliases, add them too
			
			if(not aliases is None and isinstance(aliases, (list,) )):
				self.log.debug("Command '{}': Found aliases {}".format(command_name, aliases))
				for alias in aliases:
					self.commands[alias] = command_obj
			else:
				self.log.debug("Command '{}': No aliases".format(command_name, aliases))

		# Finally after all commands have been initialized then add the help command
		self.commands['help'] = Help(self)

		# Done initializing
		self.log.info("...Commands initialized: {}".format(
				list( self.commands.keys()) 
			)
		)

	def _connect(self):
		"""Initiates connection with OBS Websockets, and will raise an exception 
		if it fails to connect for any reason whatsoever
		"""
		self.log.info("Trying to connect to OBS Websockets...")

		try:
				self.client = obswebsocket.obsws(self.host, self.port, self.password)
				self.client.connect()
				self.log.info("...Connected to OBS Websockets at {}:{}".format(self.host, self.port))
		except Exception as e:
			self.log.error("Could not initialize connection at {}:{} to OBS Websockets! Exception: {}".format(self.host, self.port, e))
			raise