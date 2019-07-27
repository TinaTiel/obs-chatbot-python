from bot.Result import *
import logging
import obswebsocket
import random

class ActionBase():

	def __init__(self, parent=None, lvl=0, **kwargs):
		self.log = logging.getLogger(__name__)
		self.parent = parent
		self.lvl = lvl
		allows = kwargs.get('allows', [])
		args = kwargs.get('args', None)
		if(args is None):
			raise ValueError("Action is missing 'args' configuration. Config provided: {}".format(kwargs))

		self.allows = []
		self.add_allows(allows if isinstance(allows, list) else [])
		#self.args = args
		self._init_args(args)

	def __repr__(self):
		return "{}{}={{args: {}}}".format("\t"*(self.lvl), self.__class__.__name__, str(self.args))

	def execute(self, user, user_args):
		if(not self._permit(user)):
			return Result(State.FAILURE, ["Failed allows"])
		self._execute(user, user_args)
		return Result(State.SUCCESS)

	def add_allows(self, allows):
		for allow in allows:
			self.allows.append(allow)
			allow.action = self

	def _permit(self, user):
		for allow in self.allows:
			if not allow.permit(user):
				return False
		return True

	def _init_args(self, args):
		self.args = args

	def _execute(self, user, args):
		pass

class DummyAction(ActionBase):
	'''A dummy Action class
	that takes args provided
	'''
	def __init__(self, parent=None, lvl=0, **kwargs):
		self.allows = []
		self.args = {}

	def _init_args(self):
		pass

	def _execute(self, user, user_args):
		pass


class ShowSource(ActionBase):

	def _init_args(self, args):
		self.source = args.get('source', None)
		self.duration = args.get('duration', None) # Optional
		self.scene = args.get('scene', None) # Optional
		self.pick_from_group = args.get('pick_from_group', False) # Unless specified, assume False

		if(self.source is None):
			raise ValueError("Args error, missing 'source' for command")

		if(self.duration is not None and self.duration < 0):
			raise ValueError("Args error, duration must be greater than zero")
		# If picking from the group (rather than hiding/showing the entire group contents), 
		# then try to get the items in the group and store them.
		if(isinstance(self.source, list)):
			self.pickable_items = self.source
			return

		try:
			self.picked_items = []
			self.pickable_items = [self.source]
			if(self.pick_from_group):
				self.log.debug("Group picking enabled")
				try:
					import bot.Context as ctx
					source_settings = ctx.obs_client.client.call(obswebsocket.requests.GetSourceSettings(self.source))
				except Exception as e:
					raise ValueError("Group picking enabled, but could not find group {} in OBS".format(self.source))
				if(source_settings):
					self.log.debug("Found source settings on source {}: {}".format(self.source, source_settings))
					items = source_settings.getSourcesettings().get('items', None)
					if(items and len(items)>0): #If this is incorrect, restart OBS
						self.pickable_items = list(map(lambda item: item.get('name'), items)) 
			self.log.debug("Pickable items are: {}".format(self.pickable_items))
		except Exception as e:
			raise ValueError("OBS/Config Error, specified source may not exist in OBS. Error: {}".format(e))

	def _execute(self, user, user_args):
		import bot.Context as ctx
		# get the random choice if applicable
		if(len(self.pickable_items) == 0):
			self.pickable_items = self.picked_items
			self.picked_items = []

		choice = self.pickable_items.pop(random.randrange(len(self.pickable_items)))
		self.picked_items.append(choice)

		# show the scene
		res = ctx.obs_client.client.call(obswebsocket.requests.SetSceneItemRender(choice, True, self.scene))
		if(res.status == False):
			msg = "Could not show scene item {}! Error: {}".format(choice, res.datain['error'])
			self.log.warn(msg)
			#self._twitch_failed()
			return Result(State.FAILURE, msg)

		# if a duration was specified then sleep and then hide the scene
		if(self.duration is not None):
			# wait the specified duration
			time.sleep(self.duration)

			# hide the scene again
			res = ctx.obs_client.client.call(obswebsocket.requests.SetSceneItemRender(choice, False, self.scene))
			if(res.status == False):
				msg = "Could not hide scene item {} after specified duration! Error: {}".format(choice, res.datain['error'])
				self.log.warn(msg)
				#self._twitch_failed()
				return Result(State.FAILURE, msg)

		#self._twitch_done()
		return Result(State.SUCCESS)