import unittest
from unittest.mock import *
from bot import *

class TestManagers(unittest.TestCase):

	def setUp(self):
		pass

	# def test_name_and_executor_are_required(self):

	# 	command_manager = CommandManager()
	# 	self.assertRaises(ValueError, command_manager.register, {})
	# 	self.assertRaises(ValueError, command_manager.register, {"name": "foo"})
	# 	self.assertRaises(ValueError, command_manager.register, {"name": "foo", "descr": ""})
	# 	self.assertRaises(ValueError, command_manager.register, {"name": "foo", "descr": "", "aliases": []})
	# 	self.assertRaises(ValueError, command_manager.register, {"name": "foo", "descr": "", "aliases": [], "allow":[]})


	# 	# Otherwise if all are required
	# 	# No errors occur
	# 	try:
	# 		command_manager.register({'name': 'foo', 'exec': {}, 'allow': [] })
	# 	except ValueError:
	# 		self.fail("command manager register() failed unexpectedly!")

if __name__ == '__main__':
	unittest.main()