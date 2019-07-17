from bot.Result import *
from collections import deque

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

class GatedExecutor():
	def __init__(self, actions):
		self.executed = list()
		self.actions = deque(actions)

	def execute(self, user, args_list):
		# If this was initialized with no actions at all, do nothing
		if(len(self.actions) == 0 and len(self.executed) == 0):
			return Result(State.SUCCESS)

		# Otherwise if just the actions are empty, then re-initialize them
		if(len(self.actions) == 0):
			while(len(self.executed) > 0):
				self.actions.appendleft(self.executed.pop())

		# process the first item in the queue
		# if it executes successfully then added it to the executed queue
		# else put it back in the queue
		selected = self.actions.popleft()
		result = selected.execute(user, args_list)
		if(result.state != State.SUCCESS):
			self.actions.appendleft(selected)
		else:
			self.executed.append(selected)

		return Result(result.state, [result])