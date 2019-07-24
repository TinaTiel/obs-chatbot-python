import unittest
from unittest.mock import *
from bot import *

class TestCommands(unittest.TestCase):

	def setUp(self):
		self.allow_always = Allow()
		self.allow_always.permit = MagicMock(return_value=True)
		

	def test_allows_none(self):
		'''
		A Command having no allows never executes
		'''
		user = User("foo")
		executor = DummyExecutor(**{"args": {"actions":[]}})
		executor.execute = MagicMock()

		# Given a command with no allows
		commandNoAllows = Command("name", executor, [])
		self.assertEqual(0, len(commandNoAllows.allows))

		# When executed
		result = commandNoAllows.execute(user, None)

		# Then the command does NOT execute any available actions and returns a FAILURE
		executor.execute.assert_not_called()
		self.assertEqual(State.FAILURE, result.state)

	def test_allows_passing(self):
		'''
		A Command having all passing allows executes
		'''
		user = User("foo")
		executor = DummyExecutor(**{"args": {"actions":[]}})
		executor.execute = MagicMock()

		# Given a command with passing allows
		allowPass = Allow()
		allowPass.permit = MagicMock(return_value=True)
		commandPass = Command("name", executor, [allowPass, allowPass])
		self.assertEqual(2, len(commandPass.allows))

		# When executed
		result = commandPass.execute(user, None)

		# Then the command executes
		executor.execute.assert_called()

	def test_allows_failing(self):
		'''
		A Command having any failing allow doesn't execute
		'''
		user = User("foo")
		executor = DummyExecutor(**{"args": {"actions":[]}})
		executor.execute = MagicMock()

		# Given a command with a failing allow
		allowPass = Allow()
		allowPass.permit = MagicMock(return_value=True)
		allowFail = Allow()
		allowFail.permit = MagicMock(return_value=False)
		commandFail = Command("name", executor, [allowPass, allowFail, allowPass])
		self.assertEqual(3, len(commandFail.allows))

		# When executed
		result = commandFail.execute(user, None)

		# Then the command does NOT execute any available actions and returns a FAILURE
		executor.execute.assert_not_called()
		self.assertEqual(State.FAILURE, result.state)

	# def test_execution_many_args(self):
	# 	'''
	# 	Arguments are separated by spaces
	# 	and can be grouped by quotes
	# 	'''
	# 	# Given a command
	# 	user = User("foo")
	# 	executor = Executor([])
	# 	executor.execute = MagicMock()
	# 	command = Command("name", executor, [self.allow_always])
		
	# 	# When the command is executed with many args in one string
	# 	command.execute(user, "foo 'bar bar' \"baz baz\"")

	# 	# Then the executor is executed with a list of arg strings
	# 	executor.execute.assert_called_with(user, ["foo", "bar bar", "baz baz"])

	# def test_actions_no_args(self):
	# 	'''
	# 	No arguments can be supplied
	# 	'''
	# 	# Given a command with many actions
	# 	user = User("foo")
	# 	executor = Executor([])
	# 	executor.execute = MagicMock()
	# 	command = Command("name", executor, [self.allow_always])
		
	# 	# When the command is executed with many args in one string
	# 	command.execute(user, None)

	# 	# Then the executor is executed with a list of arg strings
	# 	executor.execute.assert_called_with(user, [])

if __name__ == '__main__':
	unittest.main()