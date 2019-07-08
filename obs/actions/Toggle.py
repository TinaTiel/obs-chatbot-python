import obswebsocket, obswebsocket.requests
import logging
import time
import random
from obs.actions.Action import Action
from obs.actions.ShowSource import ShowSource
from obs.actions.HideSource import HideSource
from obs.Permission import Permission

class Toggle(Action):

	def __init__(self, obs_client, command_name, aliases, description, permission, min_votes, args):
		"""Initializes this class, see Action.py
		"""
		super().__init__(obs_client, command_name, aliases, description, permission, min_votes, args)
		self.log = logging.getLogger(__name__)
		self._init_args(args)

	def execute(self, user):
		"""Shows a scene item, such as an image or video, and then hides it after
		a specified duration
		"""

		# Check user permissions and votes
		if(not (
			self._has_permission(user) 
			and self._has_enough_votes(user) 
			)
		):
			self._twitch_failed()
			return False
		
		# finally execute the command
		if(not self.toggle_off_obj2.execute(user)):
			return False
		if(not self.toggle_on_obj1.execute(user)):
			return False

		# if a duration was specified then sleep and then hide the scene
		if(self.duration is not None):
			# wait the specified duration
			time.sleep(self.duration)

			if(not self.toggle_on_obj2.execute(user)):
				return False
			if(not self.toggle_off_obj1.execute(user)):
				return False

		self._twitch_done()
		return True

	def _init_args(self, args):
		"""This validates the arguments are valid for this instance, 
		and raises a ValueError if they aren't.

		Mandatory args:
		scene item (string): Name of the scene to show.
		
		Optional args:
		scene (string): Name of scene where scene item is nested. If not provided, 
									  then the current scene is used. 
		duration (int): Duration (seconds) to show scene.
		"""


		self.duration = args.get('duration', None) # Optional
		self.toggle_on = args.get('toggle_on', None)
		self.toggle_off = args.get('toggle_off', None)

		if(self.toggle_on is None or self.toggle_off is None):
			raise ValueError("Command {}: Args error, missing 'toggle_on' or 'toggle_off'".format(self.command_name))

		if(self.duration is not None and self.duration < 0):
			raise ValueError("Command {}: Args error, duration must be greater than zero".format(self.command_name))

		# Try to instantiate the toggle on and off action classes
		self.log.debug("Command {}: Toggle on/off args are {}/{}".format(self.command_name, self.toggle_on, self.toggle_off))
		try:
			self.toggle_on_obj1 = ShowSource(
				self.obs_client, 
				self.command_name + "_toggle_on1", 
				None, 
				"Toggle On for {}".format(self.command_name), 
				Permission.EVERYONE, 
				0,
				self.toggle_on)
		except ValueError as e:
			self.log.error("ERROR: " + e)
			raise e

		try:
			self.toggle_off_obj1 = HideSource(
				self.obs_client, 
				self.command_name + "_toggle_off1", 
				None, 
				"Toggle On for {}".format(self.command_name), 
				Permission.EVERYONE, 
				0,
				self.toggle_on)
		except ValueError as e:
			self.log.error("ERROR: " + e)
			raise e

		try:
			self.toggle_on_obj2 = ShowSource(
				self.obs_client, 
				self.command_name + "_toggle_on2", 
				None, 
				"Toggle On for {}".format(self.command_name), 
				Permission.EVERYONE, 
				0,
				self.toggle_off)
		except ValueError as e:
			self.log.error("ERROR: " + e)
			raise e

		try:
			self.toggle_off_obj2 = HideSource(
				self.obs_client, 
				self.command_name + "_toggle_off2", 
				None, 
				"Toggle On for {}".format(self.command_name), 
				Permission.EVERYONE, 
				0,
				self.toggle_off)
		except ValueError as e:
			self.log.error("ERROR: " + e)
			raise e

		# disable randomizers to keep it simple for now
		if(isinstance(self.toggle_on_obj1.source, list) or isinstance(self.toggle_off_obj1.source, list)):
			self.toggle_on_obj1.source = self.toggle_on_obj1.source[0]
			self.toggle_off_obj1.source = self.toggle_off_obj1.source[0]
		
		if(isinstance(self.toggle_on_obj2.source, list) or isinstance(self.toggle_off_obj2.source, list)):
			self.toggle_on_obj2.source = self.toggle_on_obj2.source[0]
			self.toggle_off_obj2.source = self.toggle_off_obj2.source[0]

		self.toggle_on_obj1.pick_from_group = False
		self.toggle_off_obj1.pick_from_group = False
		self.toggle_on_obj2.pick_from_group = False
		self.toggle_off_obj2.pick_from_group = False

		# Disable any duration args, it's controlled here instead
		self.toggle_on_obj1.duration = None
		self.toggle_off_obj1.duration = None
		self.toggle_on_obj2.duration = None
		self.toggle_off_obj2.duration = None