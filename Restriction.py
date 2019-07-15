from Permission import *

class Restriction():
	def __init__(self):
		pass

	def permit(self, user):
		pass

class RestrictionUserStatus(Restriction):
	'''
	Restriction is based on user status
	'''
	def __init__(self, min_permission=Permission.BROADCASTER):
		self.min_permission = min_permission

	def permit(self, user):

		if(user.broadcaster):
			user_status = Permission.BROADCASTER
		elif(user.moderator):
			user_status = Permission.MODERATOR
		elif(user.subscriber):
			user_status = Permission.SUBSCRIBER
		elif(user.follower):
			user_status = Permission.FOLLOWER
		else:
			user_status = Permission.EVERYONE

		return user_status >= self.min_permission