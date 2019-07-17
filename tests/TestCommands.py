import unittest
from unittest.mock import *
from bot import *

class TestCommands(unittest.TestCase):

	def setUp(self):
		pass

	def test_restrictions_have_parent_command_reference(self):
		'''
		Each restriction added to a command must have a reference to its parent command
		'''
		# Given a command with several restrictions
		r1 = Restriction()
		r2 = Restriction()
		r3 = Restriction()
		command = Command("command name", "descr", ["alias"], None, [r1, r2, r3])

		# Each restriction has a reference to the command
		self.assertEqual("command name", r1.command.name)
		self.assertEqual("command name", r2.command.name)
		self.assertEqual("command name", r3.command.name)

	# def test_actions_have_parent_command_reference(self):
	# 	'''
	# 	Each restriction added to a command must have a reference to its parent command
	# 	'''
	# 	# Given a command with several restrictions
	# 	a1 = Action()
	# 	a2 = Action()
	# 	a3 = Action()
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
		action = Action()
		action.execute = MagicMock()

		# Given a command with no restrictions
		commandNoRestrictions = Command("name", "descr", ["alias"], [action], None)
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
		action = Action()
		action.execute = MagicMock()

		# Given a command with passing restrictions
		restrictionPass = Restriction()
		restrictionPass.permit = MagicMock(return_value=True)
		commandPass = Command("name", "descr", ["alias"], [action], [restrictionPass, restrictionPass])
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
		action = Action()
		action.execute = MagicMock()

		# Given a command with a failing restriction
		restrictionPass = Restriction()
		restrictionPass.permit = MagicMock(return_value=True)
		restrictionFail = Restriction()
		restrictionFail.permit = MagicMock(return_value=False)
		commandFail = Command("name", "descr", ["alias"], [action], [restrictionPass, restrictionFail, restrictionPass])
		self.assertEqual(3, len(commandFail.restrictions))

		# When executed
		result = commandFail.execute(user, None).state

		# Then the command does NOT execute any available actions
		self.assertEqual(State.FAILURE, result)
		commandFail.actions[0].execute.assert_not_called()

	# def test_any_failing_action_causes_command_failure(self):
	# 	'''
	# 	If any command fails during execution then the command as a whole should fail
	# 	'''
	# 	# Given a command with several actions

	# 	actionPass1 = Action()
	# 	actionPass1.execute = MagicMock(return_value=Result(State.SUCCESS))

	# 	actionFail = Action()
	# 	actionFail.execute = MagicMock(return_value=Result(State.FAILURE))

	# 	actionPass2 = Action()
	# 	actionPass2.execute = MagicMock(return_value=Result(State.SUCCESS))

	# 	command = Command("name", "descr", ["alias"], [actionPass1, actionFail, actionPass2], None)

	# 	# When executed with a failing action
	# 	result = command.execute(User("foo"), None)

	# 	# Then the command reports a failure and only the first two commands executed
	# 	self.assertEqual(State.FAILURE, result.state)
	# 	actionPass1.execute.assert_called_once()
	# 	actionFail.execute.assert_called_once()
	# 	actionPass2.execute.assert_not_called()

	# def test_actions_many_args(self):
	# 	'''
	# 	Arguments are separated by spaces
	# 	and can be grouped by quotes
	# 	'''
	# 	# Given a command with many actions
	# 	user = User("foo")
	# 	restriction = Restriction()
	# 	action1 = Action()
	# 	action2 = Action()
	# 	action3 = Action()
	# 	action1.execute = MagicMock()
	# 	action2.execute = MagicMock()
	# 	action3.execute = MagicMock()
	# 	command = Command("name", "descr", ["alias"], [action1, action2, action3], restriction)
	# 	self.assertEqual(3, len(command.actions))
		
	# 	# When the command is executed with many args
	# 	command.execute(user, "foo 'bar bar' \"baz baz\"")

	# 	# Then each action is executed with those args
	# 	for action in command.actions:
	# 		action.execute.assert_called_with(user, ["foo", "bar bar", "baz baz"])

	# def test_actions_no_args(self):
	# 		'''
	# 		No arguments can be supplied
	# 		'''
	# 		# Given a command with many actions
	# 		user = User("foo")
	# 		restriction = Restriction()
	# 		action1 = Action()
	# 		action2 = Action()
	# 		action3 = Action()
	# 		action1.execute = MagicMock()
	# 		action2.execute = MagicMock()
	# 		action3.execute = MagicMock()
	# 		command = Command("name", "descr", ["alias"], [action1, action2, action3], restriction)
	# 		self.assertEqual(3, len(command.actions))
			
	# 		# When the command is executed with no args
	# 		command.execute(user, None)

	# 		# Then each action is executed with no args
	# 		for action in command.actions:
	# 			action.execute.assert_called_with(user, [])

if __name__ == '__main__':
	unittest.main()