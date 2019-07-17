from bot.Result import *

class Executor():
	def __init__(self, actions):
		self.actions = actions

	def execute(self, user, args_list):
		results = []
		for action in self.actions:
			result = action.execute(user, args_list)
			results.append(result)

			# If an action failed, exit early
			if(result.state == State.FAILURE):
				return Result(State.FAILURE, results)

		# Return success
		return Result(State.SUCCESS, results)

class ExecutorGated():
	def __init__(self, actions):
		pass

	def execute(self, user, args_list):
		pass