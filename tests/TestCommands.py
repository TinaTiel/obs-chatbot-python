import unittest
from unittest.mock import *
from bot import *

class TestCommands(unittest.TestCase):

	def setUp(self):
		pass

	# def test_restrictions_have_parent_command_reference(self):
	# 	'''
	# 	Each restriction added to a command must have a reference to its parent command
	# 	'''
	# 	# Given a command with several restrictions
	# 	r1 = Restriction()
	# 	r2 = Restriction()
	# 	r3 = Restriction()
	# 	command = Command("command name", "descr", ["alias"], None, [r1, r2, r3])

	# 	# Each restriction has a reference to the command
	# 	self.assertEqual("command name", r1.command.name)
	# 	self.assertEqual("command name", r2.command.name)
	# 	self.assertEqual("command name", r3.command.name)

	# def test_actions_have_parent_command_reference(self):
	# 	'''
	# 	Each restriction added to a command must have a reference to its parent command
	# 	'''
	# 	# Given a command with several restrictions
	# 	a1 = Executor([])
	# 	a2 = Executor([])
	# 	a3 = Executor([])
	# 	command = Command("command name", "descr", ["alias"], [a1, a2, a3], None)

	# 	# Each restriction has a reference to the command
	# 	self.assertEqual("command name", a1.command.name)
	# 	self.assertEqual("command name", a2.command.name)
	# 	self.assertEqual("command name", a3.command.name)

	def test_restrictions_none(self):
		'''
		A Command having no restrictions always executes
		'''
		user = User("foo")
		executor = Executor([])
		executor.execute = MagicMock()

		# Given a command with no restrictions
		commandNoRestrictions = Command("name", "descr", ["alias"], executor, None)
		self.assertEqual(0, len(commandNoRestrictions.restrictions))

		# When executed
		result = commandNoRestrictions.execute(user, None).state

		# Then the command excecutes available actions & returns SUCCESS
		self.assertEqual(State.SUCCESS, result)
		commandNoRestrictions.actions[0].execute.assert_called()

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
		commandPass = Command("name", "descr", ["alias"], executor, [restrictionPass, restrictionPass])
		self.assertEqual(2, len(commandPass.restrictions))

		# When executed
		result = commandPass.execute(user, None).state

		# Then the command executes available actions
		self.assertEqual(State.SUCCESS, result)
		commandPass.actions[0].execute.assert_called()

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
		commandFail = Command("name", "descr", ["alias"], executor, [restrictionPass, restrictionFail, restrictionPass])
		self.assertEqual(3, len(commandFail.restrictions))

		# When executed
		result = commandFail.execute(user, None).state

		# Then the command does NOT execute any available actions
		self.assertEqual(State.FAILURE, result)
		commandFail.actions[0].execute.assert_not_called()

	def test_any_failing_executor_causes_command_failure(self):
		'''
		If any command fails during execution then the command as a whole should fail
		'''
		# Given a command with several actions

		execPass1 = Executor([])
		execPass1.execute = MagicMock(return_value=Result(State.SUCCESS))

		execFail = Executor([])
		execFail.execute = MagicMock(return_value=Result(State.FAILURE))

		execPass2 = Executor([])
		execPass2.execute = MagicMock(return_value=Result(State.SUCCESS))

		command = Command("name", "descr", ["alias"], [execPass1, execFail, execPass2], None)

		# When executed with a failing action
		result = command.execute(User("foo"), None)

		# Then the command reports a failure and only the first two commands executed
		self.assertEqual(State.FAILURE, result.state)
		execPass1.execute.assert_called_once()
		execFail.execute.assert_called_once()
		execPass2.execute.assert_not_called()

	def test_execution_many_args(self):
		'''
		Arguments are separated by spaces
		and can be grouped by quotes
		'''
		# Given a command with many actions
		user = User("foo")
		restriction = Restriction()
		executor = Executor([])
		executor.execute = MagicMock()
		command = Command("name", "descr", ["alias"], executor, restriction)
		
		# When the command is executed with many args in one string
		command.execute(user, "foo 'bar bar' \"baz baz\"")

		# Then the executor is executed with a list of arg strings
		executor.execute.assert_called_with(user, ["foo", "bar bar", "baz baz"])

	# def test_actions_no_args(self):
	# 		'''
	# 		No arguments can be supplied
	# 		'''
	# 		# Given a command with many actions
	# 		user = User("foo")
	# 		restriction = Restriction()
	# 		exec1 = Executor([])
	# 		exec2 = Executor([])
	# 		exec3 = Executor([])
	# 		exec1.execute = MagicMock()
	# 		exec2.execute = MagicMock()
	# 		exec3.execute = MagicMock()
	# 		command = Command("name", "descr", ["alias"], [exec1, exec2, exec3], restriction)
	# 		self.assertEqual(3, len(command.actions))
			
	# 		# When the command is executed with no args
	# 		command.execute(user, None)

	# 		# Then each action is executed with no args
	# 		for action in command.actions:
	# 			action.execute.assert_called_with(user, [])

if __name__ == '__main__':
	unittest.main()