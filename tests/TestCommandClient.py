import unittest
from unittest.mock import *
from bot import *

class TestCommandClient(unittest.TestCase):

	def setUp(self):
		pass

	def test_load_commands(self):
		'''
		All commands must be error free for them all to load
		'''
		# Given a Command Client
		client = CommandClient()
		client.load_command = MagicMock()

		# When a bad config is loaded then a ValueError is returned
		self.assertRaises(ValueError, client.load_commands, {})
		self.assertRaises(ValueError, client.load_commands, {'commands': "foo"})

		# When a good config with no commands, then no error
		try:
			client.load_commands({'commands': []})
		except Exception:
			self.fail("Unexpected exception")

		# Comand is loaded for every command provided when no errors
		client.load_command = MagicMock()
		client.load_commands([{}, {}, {}])
		self.assertEqual(3, client.load_command.call_count)

		# When a good config but one resulting in errors during load then a ValueError is returned
		client.load_command = MagicMock(side_effect=ValueError)
		self.assertRaises(ValueError, client.load_commands, [{}, {}, {}])

	# def test_load_command(self):
	# 	'''
	# 	Every command requires name, allows, and execute. All other stuff is optional.
	# 	'''
	# 	self.fail("not implemented")

	# def test_command_retrieval(self):
	# 	'''
	# 	A command added successfully will be accessible in the client
	# 	'''
	# 	self.fail("not implemented")

	# def test_command_disable_enable(self):
	# 	'''
	# 	Commands can be disabled/enabled during runtime and won't be available to execute
	# 	'''
	# 	self.fail("not implemented")

	# def test_command_reload(self):
	# 	'''
	# 	Commands can be reloaded during runtime, e.g. if the broadcaster changes 
	# 	something during the broadcast and wants those changes available without
	# 	restarting the entire bot.

	# 	If there is an error, the reload won't happen and a warning will be logged; the 
	# 	bot will still function as normal.
	# 	'''
	# 	self.fail("not implemented")
