from enum import Enum
import shlex

class Command():

	def __init__(self, name, description, actions, restrictions):
		self.name = name
		self.description = description
		self.actions = actions if isinstance(actions, list) else []
		self.restrictions = restrictions if isinstance(restrictions, list) else []

	def execute(self, user, args):
		results = []
		args_list = []
		if(args is not None):
			args_list = shlex.split(args)
		for action in self.actions:
			results.append(action.execute(user, args_list))
		return results


class Action():

	def __init__(self):
		pass

	def execute(self, user, args):
		pass


class Restriction():
	pass


class Result(Enum):
	FAILURE = 1
	SUCCESS = 2