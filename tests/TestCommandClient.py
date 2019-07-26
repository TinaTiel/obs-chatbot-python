import unittest
from unittest.mock import *
from bot import *

class TestCommandClient(unittest.TestCase):

	def setUp(self):
		pass

	def test_command_args(self):
		'''
		Every command requires name, allows, and execute. All other stuff is optional.
		'''
		self.fail("not implemented")

	def test_command_retrieval(self):
		'''
		A command added successfully will be accessible in the client
		'''
		self.fail("not implemented")

	def test_command_disable_enable(self):
		'''
		Commands can be disabled/enabled during runtime and won't be available to execute
		'''
		self.fail("not implemented")

	def test_command_reload(self):
		'''
		Commands can be reloaded during runtime, e.g. if the broadcaster changes 
		something during the broadcast and wants those changes available without
		restarting the entire bot.
		'''
		self.fail("not implemented")
