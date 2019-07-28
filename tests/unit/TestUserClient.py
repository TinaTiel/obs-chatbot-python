from unittest import TestCase
from unittest.mock import MagicMock
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
		# Given a fresh user client
		client = UserClient()
		client.get_user_by_username = MagicMock()
		client.create_or_update_user = MagicMock()

		# When we try to get an user by username
		user = client.get_user('foo')

		# Then get user by username is called
		self.assertEqual(1, client.get_user_by_username.call_count)
		self.assertEqual(0, client.create_or_update_user.call_count)

		# When we try to get an user by twitch_user object
		twitch_user = TwitchUser("foo",
													False,
													False,
													0,
													False,
													False)
		user = client.get_user(twitch_user)

		# Then a it tries to create or update an existing user
		self.assertEqual(1, client.get_user_by_username.call_count)
		self.assertEqual(1, client.create_or_update_user.call_count)

		# And if one tries to retrive something that isn't a string or twitch_user
		# Then a ValueError is thrown
		self.assertRaises(ValueError, client.get_user, {'name': 'foo'})

	def test_get_user_by_username(self):
		# Given a client with no users in it
		client = UserClient()
		self.assertEqual(0, len(client.users))

		# When getting an user by username
		user = client.get_user_by_username('foo')

		# Then None is returned
		self.assertEqual(None, user)

		# But when that user exists
		client.users['foo'] = User('foo')
		self.assertEqual(1, len(client.users))

		# When getting that user by username
		user = client.get_user('foo')

		# Then the user is returned
		self.assertTrue(isinstance(user, User))
		self.assertTrue('foo', user.username)
		self.assertEqual(False, user.follower)
		self.assertEqual(False, user.subscriber)
		self.assertEqual(False, user.subscriber_duration)
		self.assertEqual(False, user.moderator)
		self.assertEqual(False, user.broadcaster)
		self.assertEqual(0, user.points)

	def test_create_or_update(self):

		# Given a clean user client
		client = UserClient()
		client.create_user = MagicMock()
		client.update_user = MagicMock()
		self.assertEqual(0, len(client.users))

		# And a twitch user
		twitch_user = TwitchUser("foo",
													False,
													False,
													0,
													False,
													False)

		# When we try to create or update a twitch user
		client.create_or_update_user(twitch_user)

		# Then create_user is called
		self.assertEqual(1, client.create_user.call_count)
		self.assertEqual(0, client.update_user.call_count)

		# But if an user by that username exists
		client.users['foo'] = User('foo')
		self.assertEqual(1, len(client.users))

		# When we try to create or update a twitch user
		client.create_or_update_user(twitch_user)

		# Then update_user is called
		self.assertEqual(1, client.create_user.call_count)
		self.assertEqual(1, client.update_user.call_count)

	def test_create_user(self):
		# Given a clean client
		client = UserClient()
		self.assertEqual(0, len(client.users))

		# And a Twitch user
		twitch_user = TwitchUser("foo",
													False,
													False,
													0,
													False,
													False)

		# When we create an user
		user = client.create_user(twitch_user)

		# Then the user is created
		self.assertEqual(1, len(client.users))
		self.assertTrue(isinstance(user, User))
		self.assertEqual('foo', user.username)
		self.assertEqual(False, user.follower)
		self.assertEqual(False, user.subscriber)
		self.assertEqual(False, user.subscriber_duration)
		self.assertEqual(False, user.moderator)
		self.assertEqual(False, user.broadcaster)
		self.assertEqual(0, user.points)

	def test_update_user(self):
		# Given a client with an existing user
		client = UserClient()
		existing_user = User('foo')
		client.users['foo'] = existing_user
		self.assertEqual(1, len(client.users))

		# And an updated Twitch user (now following)
		updated_twitch_user = TwitchUser("foo",
													True,
													False,
													0,
													False,
													False)

		# When we update a Twitch user
		updated_user = client.update_user(existing_user, updated_twitch_user)

		# Then the existing user object is updated
		self.assertEqual(1, len(client.users))
		self.assertTrue(updated_user is existing_user) # same object in memory
		self.assertEqual('foo', updated_user.username)
		self.assertEqual(True, updated_user.follower)
		self.assertEqual(False, updated_user.subscriber)
		self.assertEqual(False, updated_user.subscriber_duration)
		self.assertEqual(False, updated_user.moderator)
		self.assertEqual(False, updated_user.broadcaster)
		self.assertEqual(0, updated_user.points)