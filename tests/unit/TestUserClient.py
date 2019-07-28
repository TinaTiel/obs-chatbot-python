from unittest import TestCase
from bot.clients.twitch.TwitchBotCore import TwitchUser
from bot.User import User
from bot.clients.UserClient import UserClient

class TestUserClient(TestCase):
	
	def setup(self):
		pass

	def test_user_retrieval(self):
		'''
		When creating or updating an user, it re-uses an existing instance if 
		it exists but if not will create it.
		'''
		# Given an public user named tuple from the Twitch bot (implementation may change)
		twitch_user = TwitchUser("foo",
													False,
													False,
													0,
													False,
													False)
		# And no users by that name in the user client
		client = UserClient()
		self.assertEqual(0, len(client.users))

		# When this user is upserted
		client.upsert_user(twitch_user)

		# Then a new user is created with additional metadata
		self.assertEqual(1, len(client.users))
		user = client.get_user(twitch_user['name'])
		self.assertEqual('foo', user.username)
		self.assertEqual(False, user.follower)
		self.assertEqual(False, user.subscriber)
		self.assertEqual(False, user.subscriber_dur)
		self.assertEqual(False, user.moderator)
		self.assertEqual(False, user.broadcaster)
		self.assertEqual(0, user.points)

		# When that same user but with new info is upserted again (is a follower)
		updated_twitch_user = TwitchUser("foo",
													True,
													False,
													0,
													False,
													False)
		same_user = client.upsert(updated_twitch_user)

		# Then the existing user is updated
		self.assertTrue(same_user is user) # same memory addr
		self.assertEqual('foo', same_user.username)
		self.assertEqual(True, same_user.follower)
		self.assertEqual(False, same_user.subscriber)
		self.assertEqual(False, same_user.subscriber_dur)
		self.assertEqual(False, same_user.moderator)
		self.assertEqual(False, same_user.broadcaster)
		self.assertEqual(0, same_user.points)