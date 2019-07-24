import unittest
from unittest.mock import *
from bot import *

class TestCommands(unittest.TestCase):

	def setUp(self):
		self.allow_always = Allow()
		self.allow_always.permit = MagicMock(return_value=True)

	def fake_build(self, config):
		pass

	@patch.object(Command, '_build_executor', fake_build)
	def test_allows_conf(self):
		'''
		The configuration for a single or set of Allows must have certain type and args
		'''
		# Given invalid configs, a ValueError is thrown
		executor = DummyExecutor(**{"args": {"actions":[]}})

		self.assertRaises(ValueError, Command, "name", [{}], {})
		self.assertRaises(ValueError, Command, "name", [{"type": "foo"}], {})
		self.assertRaises(ValueError, Command, "name", [{"args": {}}], {})
		self.assertRaises(ValueError, Command, "name", [{"type": "foo", "args": {}}], {})
		self.assertRaises(ValueError, Command, "name", [{"type": "foo", "args": {}}, {"type": "DummyAllow", "args": {}}], {})
		
		# But given a valid config, no error is thrown
		try:
			command = Command("name", [{"type": "DummyAllow", "args": {}}], {})
			command = Command("name", {"type": "DummyAllow", "args": {}}, {})
		except Exception:
			self.fail("Unexpected exception")

	def test_executor_conf(self):
		'''
		The executor can be either an Executor or a single Action, but not a list
		'''
		# Given a command with invalid executor / action, ValueError is thrown
		self.assertRaises(ValueError, Command, "name", [], {})
		self.assertRaises(ValueError, Command, "name", [], {"type": "foo"})
		self.assertRaises(ValueError, Command, "name", [], {"args": {}})
		self.assertRaises(ValueError, Command, "name", [], [])

		# But given a valid executor then no error is thrown
		try:
			command = Command("name", [], {"type": "DummyExecutor", "args": {}})
			command = Command("name", [], {"type": "DummyAction", "args": {}})
		except Exception:
			self.fail("Unexpected exception")
		# Or but given a valid action then no error is thrown

	@patch.object(Command, '_build_executor', fake_build)
	def test_allows_none(self):
		'''
		A Command having no allows never executes
		'''

		# Given a command with no allows
		executor = DummyExecutor(**{"args": {"actions":[]}})
		executor.execute = MagicMock()

		command = Command("name", [], {})
		command.executor = executor

		self.assertEqual(0, len(command.allows))

		# When executed
		result = command.execute(User("foo"), None)

		# Then the command does NOT execute any available actions and returns a FAILURE
		command.executor.execute.assert_not_called()
		self.assertEqual(State.FAILURE, result.state)

	def test_allows_single(self):
		'''
		A single Allow is fine, too
		'''
		self.fail("not tested yet")

	@patch.object(Command, '_build_executor', fake_build)
	def test_allows_passing(self):
		'''
		A Command having all passing allows executes
		'''

		# Given a command with passing allows
		executor = DummyExecutor(**{"args": {"actions":[]}})
		executor.execute = MagicMock()
		dummyAllow = {"type": "DummyAllow", "args": {}}

		command = Command("name", [dummyAllow, dummyAllow, dummyAllow], {})
		command.executor = executor

		self.assertEqual(3, len(command.allows))
		command.allows[0].permit = MagicMock(return_value=True)
		command.allows[1].permit = MagicMock(return_value=True)
		command.allows[2].permit = MagicMock(return_value=True)
		
		# When executed
		result = command.execute(User("foo"), None)

		# Then the command executes
		executor.execute.assert_called()

	@patch.object(Command, '_build_executor', fake_build)
	def test_allows_failing(self):
		'''
		A Command having any failing allow doesn't execute
		'''
		user = User("foo")
		executor = DummyExecutor(**{"args": {"actions":[]}})
		executor.execute = MagicMock()
		dummyAllow = {"type": "DummyAllow", "args": {}}
		command = Command("name", [dummyAllow, dummyAllow, dummyAllow], {})
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