import unittest
from unittest.mock import *
from Command import *

class TestCommands(unittest.TestCase):

	def setUp(self):
		pass

	def test_actions_args(self):
		'''
		Arguments are separated by spaces
		and can be grouped by quotes
		'''
		# Given a command with many actions
		action = Action()
		action.execute = MagicMock()
		command = Command("test", "descr", [action, action, action], None)
		self.assertEqual(3, len(command.actions))
		
		# When the command is executed with many args
		command.execute(None, "foo 'bar bar' \"baz baz\"")

		# Then each action is executed with those args
		for action in command.actions:
			action.execute.assert_called_with(None, ["foo", "bar bar", "baz baz"])

		# And when the command is executed with no args
		command.execute(None, None)

		# Then each action is executed with no args
		for action in command.actions:
			action.execute.assert_called_with(None, [])

if __name__ == '__main__':
	unittest.main()