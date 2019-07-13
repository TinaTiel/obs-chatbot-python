import logging
import time
from obs.Permission import Permission

class Permissable:

	def __init__(self, permission_str):
		#self.permission_str = permission_str
		try:
			self.permission = Permission[permission_str]
		except:
			raise ValueError("Permission string '{}' is invalid, must be one of: {}".format(
				permission_str, 
				Permission.__members__))

	def has_permission(self, user):
		"""Gets the permission level of a given user and 
		checks if their permission is at least the required permission. 
		See the Permission class; MODERATOR > SUBSCRIBER > FOLLOWER > EVERYONE
		"""
		# First determine the user's permision level
		if(user['broadcaster']):
			user_permission = Permission.BROADCASTER
		elif(user['moderator']):
			user_permission = Permission.MODERATOR
		elif(user['subscriber']):
			user_permission = Permission.SUBSCRIBER
		elif(user['follower']):
			user_permission = Permission.FOLLOWER
		else:
			user_permission = Permission.EVERYONE
		
		result = user_permission >= self.permission
		self.log.debug("User '{}' has permission {} and required permission is {}. Operation Allowed: {}".format(user['name'], user_permission, self.permission, result))

		return result