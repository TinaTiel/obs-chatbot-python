import obswebsocket, obswebsocket.requests
import logging
import time
import random
from obs.actions.Action import Action

class ShowSource(Action):

	def __init__(self, obs_client, command_name, aliases, description, permissable, votable, args):
		"""Initializes this class, see Action.py
		"""
		super().__init__(obs_client, command_name, aliases, description, permissable, votable, args)
		self.log = logging.getLogger(__name__)
		self._init_args(args)

	def execute(self, user):
		"""Shows a scene item, such as an image or video, and then hides it after
		a specified duration
		"""

		# Check user permissions and votes
		if(not (
			self.permissable.has_permission(user) 
			and self.votable.has_enough_votes(user) 
			)
		):
			self._twitch_failed()
			return False
		
		# finally execute the command
		
		# get the random choice if applicable
		if(len(self.pickable_items) == 0):
			self.pickable_items = self.picked_items
			self.picked_items = []

		choice = self.pickable_items.pop(random.randrange(len(self.pickable_items)))
		self.picked_items.append(choice)

		# show the scene
		res = self.obs_client.client.call(obswebsocket.requests.SetSceneItemRender(choice, True, self.scene))
		if(res.status == False):
			self.log.warn("Could not show scene item {}! Error: {}".format(choice, res.datain['error']))
			self._twitch_failed()
			return False

		# if a duration was specified then sleep and then hide the scene
		if(self.duration is not None):
			# wait the specified duration
			time.sleep(self.duration)

			# hide the scene again
			res = self.obs_client.client.call(obswebsocket.requests.SetSceneItemRender(choice, False, self.scene))
			if(res.status == False):
				self.log.warn("Could not hide scene item {}! Error: {}".format(choice, res.datain['error']))
				self._twitch_failed()
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
		self.source = args.get('source', None)
		self.duration = args.get('duration', None) # Optional
		self.scene = args.get('scene', None) # Optional
		self.pick_from_group = args.get('pick_from_group', False) # Unless specified, assume False

		if(self.source is None):
			raise ValueError("Command {}: Args error, missing 'source' for command".format(self.command_name))

		if(self.duration is not None and self.duration < 0):
			raise ValueError("Command {}: Args error, duration must be greater than zero".format(self.command_name))

		# If picking from the group (rather than hiding/showing the entire group contents), 
		# then try to get the items in the group and store them.
		if(isinstance(self.source, list)):
			self.pickable_items = self.source
			return

		self.picked_items = []
		self.pickable_items = [self.source]
		if(self.pick_from_group):
			self.log.debug("Command {}: Group picking enabled".format(self.command_name))
			try:
				source_settings = self.obs_client.client.call(obswebsocket.requests.GetSourceSettings(self.source))
				if(source_settings is not None):
					self.log.debug("Command {}: Found source settings on source {}: {}".format(self.command_name, self.source, source_settings))
					items = source_settings.getSourcesettings().get('items', None)
					if(items and len(items)>0): #If this is incorrect, restart OBS
						self.pickable_items = list(map(lambda item: item.get('name'), items))
			except Exception as e:
				raise ValueError("Command {}: Could not get source settings for source '{}' in scene '{}'.".format(self.command_name, self.source, self.scene))
		self.log.debug("Command {}: Pickable items are: {}".format(self.command_name, self.pickable_items))
