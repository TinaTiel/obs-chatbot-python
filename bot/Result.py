from enum import Enum

class Result():
	def __init__(self, state, messages=[]):
		self.state = state
		self.messages = messages


class State(Enum):
	FAILURE = 1
	SUCCESS = 2
	WORKING = 3