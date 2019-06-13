class SetScene():
	def __init__(self, obs_client, name, permission, args):
		self.obs_client = obs_client
		self.name = name
		self.permission = permission
		self.votes = 0

	def execute(self, user):
		res = self.client.call(obswebsocket.requests.SetCurrentScene(args['name']))
		if(res.status == False):
			self.log.warn("Could not set scene! Error: {}".format(res.datain['error']))