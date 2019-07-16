import unittest
from unittest.mock import *
from bot import *

class TestCommands(unittest.TestCase):

	def setUp(self):
		pass

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

	def test_actions_many_args(self):
		'''
		Arguments are separated by spaces
		and can be grouped by quotes
		'''
		# Given a command with many actions
		user = User("foo")
		restriction = Restriction()
		action = Action()
		action.execute = MagicMock()
		command = Command("name", "descr", ["alias"], [action, action, action], restriction)
		self.assertEqual(3, len(command.actions))
		
		# When the command is executed with many args
		command.execute(user, "foo 'bar bar' \"baz baz\"")

		# Then each action is executed with those args
		for action in command.actions:
			action.execute.assert_called_with(user, ["foo", "bar bar", "baz baz"])

	def test_actions_no_args(self):
			'''
			No arguments can be supplied
			'''
			# Given a command with many actions
			user = User("foo")
			restriction = Restriction()
			action = Action()
			action.execute = MagicMock()
			command = Command("name", "descr", ["alias"], [action, action, action], restriction)
			self.assertEqual(3, len(command.actions))
			
			# When the command is executed with no args
			command.execute(user, None)

			# Then each action is executed with no args
			for action in command.actions:
				action.execute.assert_called_with(user, [])

if __name__ == '__main__':
	unittest.main()