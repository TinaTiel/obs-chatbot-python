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
		pass