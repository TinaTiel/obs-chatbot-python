import unittest
from unittest.mock import *
from bot import *

class TestCommands(unittest.TestCase):

	def setUp(self):
		self.allow_always = DummyAllow()
		self.allow_always.permit = MagicMock(return_value=True)

	def fake_build(self, config):
		pass

	@patch.object(CommandBase, '_build_executor', fake_build)
	def test_allows_conf(self):
		'''
		The configuration for a single or set of Allows must have certain type and args
		'''
		# Given invalid configs, a ValueError is thrown
		executor = DummyExecutor(**{"args": {"actions":[]}})

		self.assertRaises(ValueError, CommandBase, "name", [{}], {})
		self.assertRaises(ValueError, CommandBase, "name", [{"type": "foo"}], {})
		self.assertRaises(ValueError, CommandBase, "name", [{"args": {}}], {})
		self.assertRaises(ValueError, CommandBase, "name", [{"type": "foo", "args": {}}], {})
		self.assertRaises(ValueError, CommandBase, "name", [{"type": "foo", "args": {}}, {"type": "DummyAllow", "args": {}}], {})
		
		# But given a valid config, no error is thrown
		try:
			command = CommandBase("name", [{"type": "DummyAllow", "args": {}}], {})
			command = CommandBase("name", {"type": "DummyAllow", "args": {}}, {})
		except Exception:
			self.fail("Unexpected exception")

	def test_executor_conf(self):
		'''
		The executor can be either an Executor or a single Action, but not a list
		'''
		# Given a command with invalid executor / action, ValueError is thrown
		self.assertRaises(ValueError, CommandBase, "name", [], {})
		self.assertRaises(ValueError, CommandBase, "name", [], {"type": "foo"})
		self.assertRaises(ValueError, CommandBase, "name", [], {"args": {}})
		self.assertRaises(ValueError, CommandBase, "name", [], [])

		# But given a valid executor then no error is thrown
		try:
			command_executor = CommandBase("name", [], {"type": "DummyExecutor", "args": {"actions": []}})
			command_action = CommandBase("name", [], {"type": "DummyAction", "args": {}})
		except Exception:
			self.fail("Unexpected exception")

		# And the executor types are as expected
		self.assertTrue(isinstance(command_executor.executor, DummyExecutor))
		self.assertTrue(isinstance(command_action.executor, DummyAction))

		# And executing results in no errors
		try:
			command_executor.execute(User("foo"), None)
			command_action.execute(User("foo"), None)
		except Exception:
			self.fail("Unexpected exception")

	@patch.object(CommandBase, '_build_executor', fake_build)
	def test_allows_none(self):
		'''
		A Command having no allows never executes
		'''

		# Given a command with no allows
		executor = DummyExecutor(**{"args": {"actions":[]}})
		executor.execute = MagicMock()

		command = CommandBase("name", [], {})
		command.executor = executor

		self.assertEqual(0, len(command.allows))

		# When executed
		result = command.execute(User("foo"), None)

		# Then the command does NOT execute any available actions and returns a FAILURE
		command.executor.execute.assert_not_called()
		self.assertEqual(State.FAILURE, result.state)

	@patch.object(CommandBase, '_build_executor', fake_build)
	def test_allows_single(self):
		'''
		A single Allow is fine, too
		'''
		# Given a command with a single Allow definition
		dummyAllow = {"type": "DummyAllow", "args": {}}
		command = CommandBase("name", dummyAllow, {})
		command.executor = DummyExecutor(**{"args": {"actions":[]}})
		command.executor.execute = MagicMock()

		# If that allow doesn't permit
		command.allows[0].permit = MagicMock(return_value=False)

		# When executed
		result = command.execute(User("foo"), None)

		# Then the command is not executed and returns a FAILURE
		command.executor.execute.assert_not_called()
		self.assertEqual(State.FAILURE, result.state)

		# And if that allow permits
		command.executor = DummyExecutor(**{"args": {"actions":[]}})
		command.executor.execute = MagicMock()
		command.allows[0].permit = MagicMock(return_value=True)
		
		# When executed
		result = command.execute(User("foo"), None)

		# Then the command executes
		command.executor.execute.assert_called()


	@patch.object(CommandBase, '_build_executor', fake_build)
	def test_allows_passing(self):
		'''
		A Command having all passing allows executes
		'''

		# Given a command with passing allows
		executor = DummyExecutor(**{"args": {"actions":[]}})
		executor.execute = MagicMock()
		dummyAllow = {"type": "DummyAllow", "args": {}}

		command = CommandBase("name", [dummyAllow, dummyAllow, dummyAllow], {})
		command.executor = executor

		self.assertEqual(3, len(command.allows))
		command.allows[0].permit = MagicMock(return_value=True)
		command.allows[1].permit = MagicMock(return_value=True)
		command.allows[2].permit = MagicMock(return_value=True)
		
		# When executed
		result = command.execute(User("foo"), None)

		# Then the command executes
		executor.execute.assert_called()

	@patch.object(CommandBase, '_build_executor', fake_build)
	def test_allows_failing(self):
		'''
		A Command having any failing allow doesn't execute
		'''
		user = User("foo")
		executor = DummyExecutor(**{"args": {"actions":[]}})
		executor.execute = MagicMock()
		dummyAllow = {"type": "DummyAllow", "args": {}}
		command = CommandBase("name", [dummyAllow, dummyAllow, dummyAllow], {})
		command.executor = executor

		self.assertEqual(3, len(command.allows))
		command.allows[0].permit = MagicMock(return_value=True)
		command.allows[1].permit = MagicMock(return_value=False)
		command.allows[2].permit = MagicMock(return_value=True)

		# When executed
		result = command.execute(user, None)

		# Then the command does NOT execute any available actions and returns a FAILURE
		executor.execute.assert_not_called()
		self.assertEqual(State.FAILURE, result.state)

	@patch.object(CommandBase, '_build_allows', fake_build)
	@patch.object(CommandBase, '_build_executor', fake_build)
	def test_execution_many_args(self):
		'''
		Arguments are separated by spaces
		and can be grouped by quotes
		'''
		# Given a command that will be executed
		user = User("foo")
		command = CommandBase("name", [], {})
		command.executor = DummyExecutor(**{"args": {"actions":[]}})
		command.executor.execute = MagicMock()
		command._permit = MagicMock(return_value=True)
		
		# When the command is executed with many args in one string
		command.execute(user, "foo 'bar bar' \"baz baz\"")

		# Then the executor is executed with a list of arg strings
		command.executor.execute.assert_called_with(user, ["foo", "bar bar", "baz baz"])

	@patch.object(CommandBase, '_build_allows', fake_build)
	@patch.object(CommandBase, '_build_executor', fake_build)
	def test_actions_no_args(self):
		'''
		No arguments can be supplied
		'''
		# Given a command that will be executed
		user = User("foo")
		command = CommandBase("name", [], {})
		command.executor = DummyExecutor(**{"args": {"actions":[]}})
		command.executor.execute = MagicMock()
		command._permit = MagicMock(return_value=True)
		
		# When the command is executed with many args in one string
		command.execute(user, None)

		# Then the executor is executed with a list of arg strings
		command.executor.execute.assert_called_with(user, [])

if __name__ == '__main__':
	unittest.main()