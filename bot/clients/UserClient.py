from bot.User import User
from bot.clients.twitch.TwitchBotCore import TwitchUser

class UserClient():
	def __init__(self):
		self.users = {}

	def get_user(self, user):
		'''
		User can be a string or TwitchUser
		If it's a string, just get the user that exists
		Otherwise update the existing object
		'''
		if(isinstance(user, str)):
			return self.get_user_by_username(user)
		elif(isinstance(user, TwitchUser)):
			return self.create_or_update_user(user)
		else:
			raise ValueError("User object isn't string or TwitchUser instance, cannot get user!")

	def get_user_by_username(self, string):
		return self.users.get(username, None)

	def create_or_update_user(self, twitch_user):
		# existing_user = self.users.get(twitch_user['name'], None)
		# if(existing_user is None):
		# 	return self._create_user(twitch_user)
		# else:
		# 	return self._update_user(existing_user, twitch_user)
		pass

	def create_user(self, twitch_user):
		pass

	def update_user(self, existing_user, twitch_user):
		pass