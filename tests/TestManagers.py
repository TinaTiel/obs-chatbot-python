import unittest
from unittest.mock import *
from bot import *

class TestManagers(unittest.TestCase):

	def setUp(self):
		pass

	def test_name_and_executor_are_required(self):

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
			self.fail("command manager register() failed unexpectedly!")

	def test_allow_params(self):
		# type and args are required
		command_manager = CommandManager()
		self.assertRaises(ValueError, command_manager.build_allow, {})
		self.assertRaises(ValueError, command_manager.build_allow, {"type": "foo"})
		self.assertRaises(ValueError, command_manager.build_allow, {"args": {}})

		# Otherwise if all are required
		# No errors occur
		try:
			command_manager.build_allow({'type': 'foo', 'args': {}})
		except ValueError:
			self.fail("command manager register() failed unexpectedly!")

if __name__ == '__main__':
	unittest.main()