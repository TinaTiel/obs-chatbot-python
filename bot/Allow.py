from bot.Permission import *

class Allow():
	def __init__(self, **kwargs):
		pass

	def permit(self, user):
		raise NotImplementedError("Tell me what the restriction is you poopyhead!")

class AllowUserStatus(Allow):
	'''
	Allow is based on user status in Twitch
	'''
	def __init__(self, **kwargs):
		self.min_status = kwargs.get('min_status', Permission.BROADCASTER)

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

		return user_status >= self.min_status

class AllowVoting(Allow):
	def __init__(self, **kwargs):
		min_votes = kwargs.get('min_votes', 9999)
		uniques = kwargs.get('uniques', True)
		# min_votes
		# uniques
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


class AllowWhitelist(Allow):
	def __init__(self, **kwargs):
		# whitelist
		whitelist = kwargs.get('whitelist', [])
		if(not isinstance(whitelist, list)):
			raise ValueError("Whitelist has to be a list")
		self.whitelist = whitelist

	def permit(self, user):
		return user.username in self.whitelist