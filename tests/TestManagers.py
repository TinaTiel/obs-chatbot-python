import unittest
from unittest.mock import *
from bot import *

class TestManagers(unittest.TestCase):

	def setUp(self):
		pass

	# def test_bad_command(self):
	# 	# Given config missing name, restrictions, or actions
	# 	# When initialized
	# 	# Expect a value error
	# 	command_manager = CommandManager()
	# 	self.assertRaises(ValueError, command_manager.register, {})
	# 	self.assertRaises(ValueError, command_manager.register, {'name': 'foo'})
	# 	self.assertRaises(ValueError, command_manager.register, {'name': 'foo', 'restrictions': []})
	# 	self.assertRaises(ValueError, command_manager.register, {'name': 'foo', 'actions': []})

	# 	# Otherwise if all are required
	# 	# No errors occur
	# 	try:
	# 		command_manager.register({'name': 'foo', 'actions': [], 'restrictions': [] })
	# 	except ValueError:
	# 		self.fail("command manager register() failed unexpectedly!")
