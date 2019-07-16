import unittest
from unittest.mock import *
from bot import *

class TestActions(unittest.TestCase):

	def setUp(self):
		pass

	def test_restrictions_have_parent_action_reference(self):
		'''
		Each restriction added to an action must have a reference to its parent action
		'''
		# Given a command with several restrictions
		r1 = Restriction()
		r2 = Restriction()
		r3 = Restriction()
		action = Action([r1, r2, r3])

		# Each restriction has a reference to the command
		self.assertEqual(action, r1.action)
		self.assertEqual(action, r2.action)
		self.assertEqual(action, r3.action)

	# def test_restrictions_none(self):
	# 	'''
	# 	A Command having no restrictions always executes
	# 	'''
	# 	user = User("foo")
	# 	action = Action()
	# 	action.execute = MagicMock()

	# 	# Given a command with no restrictions
	# 	commandNoRestrictions = Command("name", "descr", ["alias"], [action], None)
	# 	self.assertEqual(0, len(commandNoRestrictions.restrictions))

	# 	# When executed
	# 	result = commandNoRestrictions.execute(user, None).state

	# 	# Then the command excecutes available actions & returns SUCCESS
	# 	self.assertEqual(State.SUCCESS, result)
	# 	commandNoRestrictions.actions[0].execute.assert_called()

	# def test_restrictions_passing(self):
	# 	'''
	# 	A Command having all passing restrictions executes
	# 	'''
	# 	user = User("foo")
	# 	action = Action()
	# 	action.execute = MagicMock()

	# 	# Given a command with passing restrictions
	# 	restrictionPass = Restriction()
	# 	restrictionPass.permit = MagicMock(return_value=True)
	# 	commandPass = Command("name", "descr", ["alias"], [action], [restrictionPass, restrictionPass])
	# 	self.assertEqual(2, len(commandPass.restrictions))

	# 	# When executed
	# 	result = commandPass.execute(user, None).state

	# 	# Then the command executes available actions
	# 	self.assertEqual(State.SUCCESS, result)
	# 	commandPass.actions[0].execute.assert_called()

	# def test_restrictions_failing(self):
	# 	'''
	# 	A Command having any failing restriction doesn't execute
	# 	'''
	# 	user = User("foo")
	# 	action = Action()
	# 	action.execute = MagicMock()

	# 	# Given a command with a failing restriction
	# 	restrictionPass = Restriction()
	# 	restrictionPass.permit = MagicMock(return_value=True)
	# 	restrictionFail = Restriction()
	# 	restrictionFail.permit = MagicMock(return_value=False)
	# 	commandFail = Command("name", "descr", ["alias"], [action], [restrictionPass, restrictionFail, restrictionPass])
	# 	self.assertEqual(3, len(commandFail.restrictions))

	# 	# When executed
	# 	result = commandFail.execute(user, None).state

	# 	# Then the command does NOT execute any available actions
	# 	self.assertEqual(State.FAILURE, result)
	# 	commandFail.actions[0].execute.assert_not_called()