# Defines the valid permission strings that can be configured
from enum import Enum
from functools import total_ordering

@total_ordering
class Permission(Enum):
	EVERYONE = 1
	FOLLOWER = 2
	SUBSCRIBER = 3
	MODERATOR = 4
	BROADCASTER = 5

	def __lt__(self, other):
		if self.__class__ is other.__class__:
			return self.value < other.value
		return NotImplemented