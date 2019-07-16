import unittest
from unittest.mock import *
from bot.User import *
from bot.Restriction import *
from bot.Permission import *

class TestRestrictions(unittest.TestCase):

	def setUp(self):
		self.user_public = User("public")
		self.user_follower = User(username="follower", follower=True)
		self.user_subscriber = User(username="subscriber", subscriber=True)
		self.user_moderator = User(username="moderator", moderator=True)
		self.user_broadcaster = User(username="broadcaster", broadcaster=True)

	def test_restriction_userStatus_Everyone(self):
		'''
		The general public is allowed
		'''
		# Given a restriction to the general public
		restriction = RestrictionUserStatus(Permission.EVERYONE)

		# All users are permitted
		self.assertTrue(restriction.permit(self.user_public))
		self.assertTrue(restriction.permit(self.user_follower))
		self.assertTrue(restriction.permit(self.user_subscriber))
		self.assertTrue(restriction.permit(self.user_moderator))
		self.assertTrue(restriction.permit(self.user_broadcaster))

	def test_restriction_userStatus_Follower(self):
		'''
		Followers and higher are allowed
		'''
		# Given a restriction to followers
		restriction = RestrictionUserStatus(Permission.FOLLOWER)

		# Only followers and above are permitted
		self.assertFalse(restriction.permit(self.user_public))
		self.assertTrue(restriction.permit(self.user_follower))
		self.assertTrue(restriction.permit(self.user_subscriber))
		self.assertTrue(restriction.permit(self.user_moderator))
		self.assertTrue(restriction.permit(self.user_broadcaster))

	def test_restriction_userStatus_Subscriber(self):
		'''
		Subscribers and higher are allowed
		'''
		# Given a restriction to subscribers
		restriction = RestrictionUserStatus(Permission.SUBSCRIBER)

		# Only subscribers and above are permitted
		self.assertFalse(restriction.permit(self.user_public))
		self.assertFalse(restriction.permit(self.user_follower))
		self.assertTrue(restriction.permit(self.user_subscriber))
		self.assertTrue(restriction.permit(self.user_moderator))
		self.assertTrue(restriction.permit(self.user_broadcaster))

	def test_restriction_userStatus_Moderator(self):
		'''
		Moderators and higher are allowed
		'''
		# Given a restriction to moderators
		restriction = RestrictionUserStatus(Permission.MODERATOR)

		# Only moderators and above are permitted
		self.assertFalse(restriction.permit(self.user_public))
		self.assertFalse(restriction.permit(self.user_follower))
		self.assertFalse(restriction.permit(self.user_subscriber))
		self.assertTrue(restriction.permit(self.user_moderator))
		self.assertTrue(restriction.permit(self.user_broadcaster))

	def test_restriction_userStatus_Broadcaster(self):
		'''
		Only broadcaster is allowed
		'''
		# Given a restriction to broadcaster
		restriction = RestrictionUserStatus(Permission.BROADCASTER)

		# Only broadcaster is permitted
		self.assertFalse(restriction.permit(self.user_public))
		self.assertFalse(restriction.permit(self.user_follower))
		self.assertFalse(restriction.permit(self.user_subscriber))
		self.assertFalse(restriction.permit(self.user_moderator))
		self.assertTrue(restriction.permit(self.user_broadcaster))

	def test_restriction_voting_duplicates(self):
		'''
		Voting-based permission, duplicate votes allowed
		'''
		# Given vote restriction with unique votes required
		restriction = RestrictionVoting(5, False)

		# When the same user votes multiple times
		self.assertFalse(restriction.permit(self.user_public))
		self.assertFalse(restriction.permit(self.user_public))
		self.assertFalse(restriction.permit(self.user_public))

		# Then all those votes are counted
		self.assertEqual(3, len(restriction.votes))

		# And permit is True only after the min votes are met, then votes reset
		self.assertFalse(restriction.permit(self.user_public))
		self.assertEqual(4, len(restriction.votes))

		self.assertTrue(restriction.permit(self.user_public))
		self.assertEqual(0, len(restriction.votes))

	def test_restriction_voting_uniques(self):
		'''
		Voting based permission, but requires unique votes
		'''
		# Given vote restriction with unique votes required
		restriction = RestrictionVoting(5, True)

		# When the same user votes multiple times
		self.assertFalse(restriction.permit(self.user_public))
		self.assertFalse(restriction.permit(self.user_public))
		self.assertFalse(restriction.permit(self.user_public))

		# Then only unique votes are counted
		self.assertEqual(1, len(restriction.votes))
		self.assertFalse(restriction.permit(User("foo")))
		self.assertFalse(restriction.permit(User("bar")))
		self.assertFalse(restriction.permit(User("baz")))
		self.assertEqual(4, len(restriction.votes))

		self.assertTrue(restriction.permit(User("trigger")))
		self.assertEqual(0, len(restriction.votes))
		# But when unique voters vote then it is counted and triggers permit

	def test_restriction_whitelist(self):
		'''
		Whitelist based restriction, good for makeshift integrations
		such as whitelisting Patreons or otherwise specific folks
		'''

		# Given a whitelist
		whitelist = ["foo"]
		restriction = RestrictionWhitelist(whitelist)

		# An user not a member of the whitelist is denied
		self.assertFalse(restriction.permit(User("bar")))

		# But an user belonging to the whitelist is allowed
		self.assertTrue(restriction.permit(User("foo")))
