import unittest
from unittest.mock import *
from bot import *

class TestCommands(unittest.TestCase):

	def setUp(self):
		pass

	def test_restrictions_none(self):
		'''
		A Command having no restrictions never executes
		'''
		user = User("foo")
		executor = Executor([])
		executor.execute = MagicMock()

		# Given a command with no restrictions
		commandNoRestrictions = Command("name", executor)
		self.assertEqual(0, len(commandNoRestrictions.restrictions))

		# When executed
		result = commandNoRestrictions.execute(user, None)

		# Then the command does NOT execute any available actions and returns a FAILURE
		executor.execute.assert_not_called()
		self.assertEqual(State.FAILURE, result.state)

	def test_restrictions_passing(self):
		'''
		A Command having all passing restrictions executes
		'''
		user = User("foo")
		executor = Executor([])
		executor.execute = MagicMock()

		# Given a command with passing restrictions
		restrictionPass = Restriction()
		restrictionPass.permit = MagicMock(return_value=True)
		commandPass = Command("name", executor, [restrictionPass, restrictionPass])
		self.assertEqual(2, len(commandPass.restrictions))

		# When executed
		result = commandPass.execute(user, None)

		# Then the command executes
		executor.execute.assert_called()

	def test_restrictions_failing(self):
		'''
		A Command having any failing restriction doesn't execute
		'''
		user = User("foo")
		executor = Executor([])
		executor.execute = MagicMock()

		# Given a command with a failing restriction
		restrictionPass = Restriction()
		restrictionPass.permit = MagicMock(return_value=True)
		restrictionFail = Restriction()
		restrictionFail.permit = MagicMock(return_value=False)
		commandFail = Command("name", executor, [restrictionPass, restrictionFail, restrictionPass])
		self.assertEqual(3, len(commandFail.restrictions))

		# When executed
		result = commandFail.execute(user, None)

		# Then the command does NOT execute any available actions and returns a FAILURE
		executor.execute.assert_not_called()
		self.assertEqual(State.FAILURE, result.state)

	def test_execution_many_args(self):
		'''
		Arguments are separated by spaces
		and can be grouped by quotes
		'''
		# Given a command
		user = User("foo")
		executor = Executor([])
		executor.execute = MagicMock()
		command = Command("name", executor)
		
		# When the command is executed with many args in one string
		command.execute(user, "foo 'bar bar' \"baz baz\"")

		# Then the executor is executed with a list of arg strings
		executor.execute.assert_called_with(user, ["foo", "bar bar", "baz baz"])

	def test_actions_no_args(self):
		'''
		No arguments can be supplied
		'''
		# Given a command with many actions
		user = User("foo")
		executor = Executor([])
		executor.execute = MagicMock()
		command = Command("name", executor)
		
		# When the command is executed with many args in one string
		command.execute(user, None)

		# Then the executor is executed with a list of arg strings
		executor.execute.assert_called_with(user, [])

if __name__ == '__main__':
	unittest.main()