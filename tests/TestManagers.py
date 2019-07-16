import unittest
from unittest.mock import *
from bot import *

class TestManagers(unittest.TestCase):

	def setUp(self):
		pass

	def test_bad_command(self):
		# Given config missing name, restrictions, or actions
		# When initialized
		# Expect a value error

		self.assertRaises(ValueError, CommandManager, {})
		self.assertRaises(ValueError, CommandManager, {'name': 'foo'})
		self.assertRaises(ValueError, CommandManager, {'name': 'foo', 'restrictions': []})
		self.assertRaises(ValueError, CommandManager, {'name': 'foo', 'actions': []})
		self.assertNotRaises(ValueError, CommandManager, {'name': 'foo', 'requirements': [], 'actions': []})

		# Otherwise if all are required

		# When initialized

		# No errors occur
