from enum import Enum

class Command():

	def __init__(self, name, description, actions, restrictions):
		self.name = name
		self.description = description
		self.actions = actions
		self.restrictions = restrictions

	def execute(self, user, args):
		results = []
		for action in self.actions:
			results.append(action.execute(user, args.split(" ")))
		return results


class Action():

	def __init__(self):
		pass

	def execute(self, user, args):
		return Result.SUCCESS


class Resriction():
	pass


class Result(Enum):
	FAILURE = 1
	SUCCESS = 2