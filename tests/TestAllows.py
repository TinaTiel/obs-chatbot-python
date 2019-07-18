import unittest
from unittest.mock import *
from bot import *

class TestAllows(unittest.TestCase):

	def setUp(self):
		self.user_public = User("public")
		self.user_follower = User(username="follower", follower=True)
		self.user_subscriber = User(username="subscriber", subscriber=True)
		self.user_moderator = User(username="moderator", moderator=True)
		self.user_broadcaster = User(username="broadcaster", broadcaster=True)

	def test_allow_userStatus_valid_status(self):
		# Given an valid user status, a ValueError is thrown
		self.assertRaises(ValueError, AllowUserStatus, **{"min_status": "FOOBARBAZ"})

		# Given a valid user status, no error
		try:
			allow = AllowUserStatus(**{"min_status": "EVERYONE"})
		except ValueError:
			self.fail("Instantiating AllowUserStatus failed unexpectedly!")


	# def test_allow_userStatus_Everyone(self):
	# 	'''
	# 	The general public is allowed
	# 	'''
	# 	# Given a allow to the general public
	# 	allow = AllowUserStatus(**{"min_status": Permission.EVERYONE})

	# 	# All users are permitted
	# 	self.assertTrue(allow.permit(self.user_public))
	# 	self.assertTrue(allow.permit(self.user_follower))
	# 	self.assertTrue(allow.permit(self.user_subscriber))
	# 	self.assertTrue(allow.permit(self.user_moderator))
	# 	self.assertTrue(allow.permit(self.user_broadcaster))

	# def test_allow_userStatus_Follower(self):
	# 	'''
	# 	Followers and higher are allowed
	# 	'''
	# 	# Given a allow to followers
	# 	allow = AllowUserStatus(**{"min_status": Permission.FOLLOWER})

	# 	# Only followers and above are permitted
	# 	self.assertFalse(allow.permit(self.user_public))
	# 	self.assertTrue(allow.permit(self.user_follower))
	# 	self.assertTrue(allow.permit(self.user_subscriber))
	# 	self.assertTrue(allow.permit(self.user_moderator))
	# 	self.assertTrue(allow.permit(self.user_broadcaster))

	# def test_allow_userStatus_Subscriber(self):
	# 	'''
	# 	Subscribers and higher are allowed
	# 	'''
	# 	# Given a allow to subscribers
	# 	allow = AllowUserStatus(**{"min_status": Permission.SUBSCRIBER})

	# 	# Only subscribers and above are permitted
	# 	self.assertFalse(allow.permit(self.user_public))
	# 	self.assertFalse(allow.permit(self.user_follower))
	# 	self.assertTrue(allow.permit(self.user_subscriber))
	# 	self.assertTrue(allow.permit(self.user_moderator))
	# 	self.assertTrue(allow.permit(self.user_broadcaster))

	# def test_allow_userStatus_Moderator(self):
	# 	'''
	# 	Moderators and higher are allowed
	# 	'''
	# 	# Given a allow to moderators
	# 	allow = AllowUserStatus(**{"min_status": Permission.MODERATOR})

	# 	# Only moderators and above are permitted
	# 	self.assertFalse(allow.permit(self.user_public))
	# 	self.assertFalse(allow.permit(self.user_follower))
	# 	self.assertFalse(allow.permit(self.user_subscriber))
	# 	self.assertTrue(allow.permit(self.user_moderator))
	# 	self.assertTrue(allow.permit(self.user_broadcaster))

	# def test_allow_userStatus_Broadcaster(self):
	# 	'''
	# 	Only broadcaster is allowed
	# 	'''
	# 	# Given a allow to broadcaster
	# 	allow = AllowUserStatus(**{"min_status": Permission.BROADCASTER})

	# 	# Only broadcaster is permitted
	# 	self.assertFalse(allow.permit(self.user_public))
	# 	self.assertFalse(allow.permit(self.user_follower))
	# 	self.assertFalse(allow.permit(self.user_subscriber))
	# 	self.assertFalse(allow.permit(self.user_moderator))
	# 	self.assertTrue(allow.permit(self.user_broadcaster))

	# def test_allow_voting_duplicates(self):
	# 	'''
	# 	Voting-based permission, duplicate votes allowed
	# 	'''
	# 	# Given vote allow with unique votes required
	# 	allow = AllowVoting(**{"min_votes": 5, "uniques": False})

	# 	# When the same user votes multiple times
	# 	self.assertFalse(allow.permit(self.user_public))
	# 	self.assertFalse(allow.permit(self.user_public))
	# 	self.assertFalse(allow.permit(self.user_public))

	# 	# Then all those votes are counted
	# 	self.assertEqual(3, len(allow.votes))

	# 	# And permit is True only after the min votes are met, then votes reset
	# 	self.assertFalse(allow.permit(self.user_public))
	# 	self.assertEqual(4, len(allow.votes))

	# 	self.assertTrue(allow.permit(self.user_public))
	# 	self.assertEqual(0, len(allow.votes))

	# def test_allow_voting_uniques(self):
	# 	'''
	# 	Voting based permission, but requires unique votes
	# 	'''
	# 	# Given vote allow with unique votes required
	# 	allow = AllowVoting(**{"min_votes": 5})

	# 	# When the same user votes multiple times
	# 	self.assertFalse(allow.permit(self.user_public))
	# 	self.assertFalse(allow.permit(self.user_public))
	# 	self.assertFalse(allow.permit(self.user_public))

	# 	# Then only unique votes are counted
	# 	self.assertEqual(1, len(allow.votes))
	# 	self.assertFalse(allow.permit(User("foo")))
	# 	self.assertFalse(allow.permit(User("bar")))
	# 	self.assertFalse(allow.permit(User("baz")))
	# 	self.assertEqual(4, len(allow.votes))

	# 	self.assertTrue(allow.permit(User("trigger")))
	# 	self.assertEqual(0, len(allow.votes))
	# 	# But when unique voters vote then it is counted and triggers permit

	# def test_allow_whitelist(self):
	# 	'''
	# 	Whitelist based allow, good for makeshift integrations
	# 	such as whitelisting Patreons or otherwise specific folks
	# 	'''

	# 	# Given a whitelist
	# 	whitelist = ["foo"]
	# 	allow = AllowWhitelist(**{"whitelist": whitelist})

	# 	# An user not a member of the whitelist is denied
	# 	self.assertFalse(allow.permit(User("bar")))

	# 	# But an user belonging to the whitelist is allowed
	# 	self.assertTrue(allow.permit(User("foo")))

if __name__ == '__main__':
	unittest.main()