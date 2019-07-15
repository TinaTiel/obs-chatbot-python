import unittest
from unittest.mock import *
from User import *
from Restriction import *
from Permission import *

class TestRestrictions(unittest.TestCase):

	def setUp(self):
		self.user_public = User()
		self.user_follower = User(follower=True)
		self.user_subscriber = User(subscriber=True)
		self.user_moderator = User(moderator=True)
		self.user_broadcaster = User(broadcaster=True)

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

	# def test_restriction_userStatus_Follower(self):
	# 	self.assertTrue(False) 

	# def test_restriction_userStatus_Subscriber(self):
	# 	self.assertTrue(False) 

	# def test_restriction_userStatus_Moderator(self):
	# 	self.assertTrue(False) 

	# def test_restriction_userStatus_Broadcaster(self):
	# 	self.assertTrue(False) 

	# def test_restriction_voting(self):
	# 	self.assertTrue(False)

	# def test_restriction_userPoints(self):
	# 	self.assertTrue(False)