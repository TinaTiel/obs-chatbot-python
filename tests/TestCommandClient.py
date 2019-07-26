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
		client = CommandClientBase()
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
		client.load_commands({'commands': [{}, {}, {}]})
		self.assertEqual(3, client.load_command.call_count)

		# When a good config but one resulting in errors during load then a ValueError is returned
		client.load_command = MagicMock(side_effect=ValueError)
		self.assertRaises(ValueError, client.load_commands, {'commands': [{}, {}, {}]})

	def test_load_command(self):
		'''
		Every command requires name, allows, and execute. All other stuff is optional.
		'''
		# Given a Command Client
		client = CommandClientBase()

		# When loading an invalid command then it will raise a Value Error
		self.assertRaises(ValueError, client.load_command, {})
		self.assertRaises(ValueError, client.load_command, {'name': 'foo'})
		self.assertRaises(ValueError, client.load_command, {'allows': []})
		self.assertRaises(ValueError, client.load_command, {'action': [{}]})
		self.assertRaises(ValueError, client.load_command, {'action': {}, 'allows': []})
		self.assertRaises(ValueError, client.load_command, {'action': {}, 'name': {}})
		self.assertRaises(ValueError, client.load_command, {'name': {}, 'allows': []})
		self.assertRaises(ValueError, client.load_command, {'name': {}, 'allows': [], 'action': {'type': 'idontexist', 'args': {}}})
		self.assertRaises(ValueError, client.load_command, {'name': {}, 'allows': [{'type': 'idontexist', 'args': {}}], 'action': {'type': 'DummyAction', 'args': {}}})

		# When loading a valid command then it will not raise an error and will be accessible for retrieval
		try:
			conf = {
				'name': 'foo',
				'description': 'bar',
				'aliases': ['baz'],
				'allows': [
					{
						'type': 'DummyAllow',
						'args': {}
					}
				],
				'action': {
					'type': 'DummyExecutor',
					'args': {}
				}
			}
			client.load_command(conf)
		except Exception:
			self.fail('unexpected exception')

		command = client.commands['foo']
		self.assertEqual('foo', command.name)
		self.assertEqual('bar', command.description)
		self.assertEqual('baz', command.aliases[0])
		self.assertEqual(1, len(command.allows))
		self.assertTrue(isinstance(command.executor, DummyExecutor))

		# And when loading a command of the same name it will be overridden
		try:
			conf = {
				'name': 'foo',
				'description': 'bar',
				'aliases': ['baz'],
				'allows': [
					{
						'type': 'DummyAllow',
						'args': {}
					}
				],
				'action': {
					'type': 'ExecutorBase',
					'args': {
						'actions': [
							{
								'type': 'DummyAction',
								'args': {}
							}
						]
					}
				}
			}
			client.load_command(conf)
		except Exception:
			self.fail('unexpected exception')

		self.assertEqual(1, len(client.commands))
		command = client.commands['foo']
		self.assertEqual('foo', command.name)
		self.assertEqual('bar', command.description)
		self.assertEqual('baz', command.aliases[0])
		self.assertEqual(1, len(command.allows))
		self.assertTrue(isinstance(command.executor, ExecutorBase))
		self.assertTrue(isinstance(command.executor.actions[0], DummyAction))

	# def test_command_execution(self):
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
