import unittest
from unittest.mock import *
from bot import *

class TestActions(unittest.TestCase):

	def setUp(self):
		pass

	def test_minimum_config(self):
		# Given a minimum set of arguments
		# Then an Action class can be substantiated
		try:
			action = Action(**{"args": {}})
		except Exception:
			self.fail("Unexpected exception")

		# And given any missing arguments
		# Then a ValueError is thrown
		self.assertRaises(ValueError, Action, **{})
		self.assertRaises(ValueError, Action, **{"allows": []})

	def test_allows_have_parent_action_reference(self):
		'''
		Each allow added to an action must have a reference to its parent action
		'''
		# Given a command with several allows
		r1 = Allow()
		r2 = Allow()
		r3 = Allow()
		action = Action(**{"allows":[r1, r2, r3], "args": {}})

		# Each allow has a reference to the command
		self.assertEqual(action, r1.action)
		self.assertEqual(action, r2.action)
		self.assertEqual(action, r3.action)

	def test_allows_none(self):
		'''
		An action having no allows always executes
		'''
		# Given an action with no allows
		action = Action(**{"args": {}})
		action._execute = MagicMock()
		self.assertEqual(0, len(action.allows))

		# It will always execute
		result = action.execute(User("foo"), None).state

		# Then the command excecutes available actions & returns SUCCESS
		self.assertEqual(State.SUCCESS, result)
		action._execute.assert_called()

	def test_allows_passing(self):
		'''
		A Command having all passing allows executes
		'''
		# Given an action with passing allows
		allowPass = Allow()
		allowPass.permit = MagicMock(return_value=True)

		action = Action(**{"allows":[allowPass], "args": {}})
		action._execute = MagicMock()
		self.assertEqual(1, len(action.allows))

		# When it executes
		result = action.execute(User("foo"), None).state

		# Then the action excecutes & returns SUCCESS
		self.assertEqual(State.SUCCESS, result)
		action._execute.assert_called()

	def test_allows_failing(self):
		'''
		A Command having any failing allow doesn't execute
		'''
		# Given an action with passing and failing allows
		allowPass = Allow()
		allowPass.permit = MagicMock(return_value=True)

		allowFail = Allow()
		allowFail.permit = MagicMock(return_value=False)

		action = Action(**{"allows":[allowPass, allowFail], "args": {}})
		action._execute = MagicMock()
		self.assertEqual(2, len(action.allows))

		# When it executes
		result = action.execute(User("foo"), None).state

		# Then the action does NOT execute & returns FAILURE
		self.assertEqual(State.FAILURE, result)
		action._execute.assert_not_called()

if __name__ == '__main__':
	unittest.main()