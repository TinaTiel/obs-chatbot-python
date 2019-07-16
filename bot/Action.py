class Action():

	def __init__(self, restrictions=[], config={}):
		self.restrictions = []
		self.add_restrictions(restrictions if isinstance(restrictions, list) else [])
		self.config = config

	def execute(self, user, args):
		pass

	def add_restrictions(self, restrictions):
		for restriction in restrictions:
			self.restrictions.append(restriction)
			restriction.action = self