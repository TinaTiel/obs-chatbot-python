from bot.Permission import *

class Restriction():
	def __init__(self):
		pass

	def permit(self, user):
		pass

class RestrictionUserStatus(Restriction):
	'''
	Restriction is based on user status in Twitch
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

class RestrictionVoting(Restriction):
	def __init__(self, min_votes, uniques=True):
		if(not isinstance(min_votes, int) or min_votes < 0):
			raise ValueError("Minimum votes must be greater than 0!")
		self.min_votes = min_votes
		self.uniques = uniques
		self._reset_votes()

	def permit(self, user):
		self._add_vote(user)
		if(len(self.votes) >= self.min_votes):
			self._reset_votes()
			return True
		else:
			return False

	def _reset_votes(self):
		if(self.uniques):
			self.votes = set()
		else:
			self.votes = list()

	def _add_vote(self, user):
		if(isinstance(self.votes, list)):
			self.votes.append(user.username)
		else:
			self.votes.add(user.username)


class RestrictionWhitelist(Restriction):
	def __init__(self, whitelist):
		if(not isinstance(whitelist, list)):
			raise ValueError("Whitelist has to be a list")
		self.whitelist = whitelist

	def permit(self, user):
		return user.username in self.whitelist

class RestrictionProgressiveVoting():
	def __init__(self, vote_mins):
		pass

	def permit(self, user):
		pass