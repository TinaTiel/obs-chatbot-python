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
		r1 = Allow()
		r2 = Allow()
		r3 = Allow()
		action = Action([r1, r2, r3])

		# Each restriction has a reference to the command
		self.assertEqual(action, r1.action)
		self.assertEqual(action, r2.action)
		self.assertEqual(action, r3.action)

	def test_restrictions_none(self):
		'''
		An action having no restrictions always executes
		'''
		# Given an action with no restrictions
		action = Action()
		action._execute = MagicMock()
		self.assertEqual(0, len(action.restrictions))

		# It will always execute
		result = action.execute(User("foo"), None).state

		# Then the command excecutes available actions & returns SUCCESS
		self.assertEqual(State.SUCCESS, result)
		action._execute.assert_called()

	def test_restrictions_passing(self):
		'''
		A Command having all passing restrictions executes
		'''
		# Given an action with passing restrictions
		restrictionPass = Allow()
		restrictionPass.permit = MagicMock(return_value=True)

		action = Action([restrictionPass])
		action._execute = MagicMock()
		self.assertEqual(1, len(action.restrictions))

		# When it executes
		result = action.execute(User("foo"), None).state

		# Then the action excecutes & returns SUCCESS
		self.assertEqual(State.SUCCESS, result)
		action._execute.assert_called()

	def test_restrictions_failing(self):
		'''
		A Command having any failing restriction doesn't execute
		'''
		# Given an action with passing and failing restrictions
		restrictionPass = Allow()
		restrictionPass.permit = MagicMock(return_value=True)

		restrictionFail = Allow()
		restrictionFail.permit = MagicMock(return_value=False)

		action = Action([restrictionPass, restrictionFail])
		action._execute = MagicMock()
		self.assertEqual(2, len(action.restrictions))

		# When it executes
		result = action.execute(User("foo"), None).state

		# Then the action does NOT execute & returns FAILURE
		self.assertEqual(State.FAILURE, result)
		action._execute.assert_not_called()

if __name__ == '__main__':
	unittest.main()