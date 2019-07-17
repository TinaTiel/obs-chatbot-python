import unittest
from unittest.mock import *
from bot import *

class TestManagers(unittest.TestCase):

	def setUp(self):
		self.known_allow_type = "AllowUserStatus"

	def fake_build(self, config):
		pass

	@patch.object(CommandManager, 'build_allow', fake_build)    # Patching out the inner methods of build_command
	@patch.object(CommandManager, 'build_executor', fake_build) # Patching out the inner methods of build_command
	def test_command_requires_name_and_execute_args(self):

		command_manager = CommandManager()
		self.assertRaises(ValueError, command_manager.build_command, {})
		self.assertRaises(ValueError, command_manager.build_command, {"name": "foo"})
		self.assertRaises(ValueError, command_manager.build_command, {"name": "foo", "descr": ""})
		self.assertRaises(ValueError, command_manager.build_command, {"name": "foo", "descr": "", "aliases": []})
		self.assertRaises(ValueError, command_manager.build_command, {"name": "foo", "descr": "", "aliases": [], "allows":[]})
		self.assertRaises(ValueError, command_manager.build_command, {"execute": {}})
		self.assertRaises(ValueError, command_manager.build_command, {"execute": {}, "descr": ""})
		self.assertRaises(ValueError, command_manager.build_command, {"execute": {}, "descr": "", "aliases": []})
		self.assertRaises(ValueError, command_manager.build_command, {"execute": {}, "descr": "", "aliases": [], "allows":[]})

		# Otherwise if all are required
		# No errors occur
		try:
			command_manager.build_command({'name': 'foo', 'execute': {}, 'allows': [] })
		except ValueError:
			self.fail("command manager build_command() failed unexpectedly!")

	def test_allow_params(self):
		# type and args are required
		command_manager = CommandManager()
		self.assertRaises(ValueError, command_manager.build_allow, {})
		self.assertRaises(ValueError, command_manager.build_allow, {"type": self.known_allow_type})
		self.assertRaises(ValueError, command_manager.build_allow, {"args": {}})

		# Otherwise if all are required
		# No errors occur
		try:
			command_manager.build_allow({'type': self.known_allow_type, 'args': {}})
		except ValueError:
			self.fail("command manager build_allow() failed unexpectedly!")

	def test_allow_params_valid_type(self):

		command_manager = CommandManager()

		# Given an invalid type, expect a ValueError
		self.assertRaises(ValueError, command_manager.build_allow, {"type": "idontexistfasdfasdfasdfasdf", "args": {}})

		# Given a valid type, expect no errors
		try:
			command_manager.build_allow({"type": self.known_allow_type, "args": {}})
		except ValueError:
			self.fail("command manager build_allow() failed unexpectedly!")

	def test_execute_params(self):
		# type and args are required
		command_manager = CommandManager()
		self.assertRaises(ValueError, command_manager.build_executor, {})
		self.assertRaises(ValueError, command_manager.build_executor, {"type": self.known_allow_type})
		self.assertRaises(ValueError, command_manager.build_executor, {"args": {}})

		# Otherwise if all are required
		# No errors occur
		try:
			command_manager.build_executor({'type': self.known_allow_type, 'args': {}})
		except ValueError:
			self.fail("command manager build_executor() failed unexpectedly!")

	def test_execute_params_valid_type(self):

		command_manager = CommandManager()

		# Given an invalid type, expect a ValueError
		self.assertRaises(ValueError, command_manager.build_executor, {"type": "asdfasdfasdfasdfasdfasdf", "args": {}})
		self.assertRaises(ValueError, command_manager.build_executor, {"type": "Action", "args": {}})

		# Otherwise given a valid type (from the Executor module), no errors
		try:
			command_manager.build_executor({"type": "ExecuteAll", "args": {}})
			command_manager.build_executor({"type": "ExecuteGated", "args": {}})
		except ValueError:
			self.fail("command manager build_executor() failed unexpectedly")


if __name__ == '__main__':
	unittest.main()