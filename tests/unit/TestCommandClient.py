import unittest
from unittest.mock import MagicMock
from bot.clients.CommandClient import CommandClientBase
from bot.User import User
from bot.Command import DummyCommand
from bot.Result import Result, State
from bot.Executor import DummyExecutor, ExecutorBase
from bot.Action import DummyAction

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

		command = client.commands['foo']
		self.assertEqual('foo', command.name)
		self.assertEqual('bar', command.description)
		self.assertEqual('baz', command.aliases[0])
		self.assertEqual(1, len(command.allows))
		self.assertTrue(isinstance(command.executor, ExecutorBase))
		self.assertTrue(isinstance(command.executor.actions[0], DummyAction))

	def test_aliases(self):
		'''
		A command can have 0 to many aliases, each should trigger the same command
		'''
		# Given a command added with aliases
		client = CommandClientBase()
		conf = {
			'name': 'foo',
			'description': '',
			'aliases': ['bar', 'baz'],
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

		# That command should be accessible from the aliases
		self.assertEqual('foo', client.commands['foo'].name)
		self.assertEqual('foo', client.commands['bar'].name)
		self.assertEqual('foo', client.commands['baz'].name)

	def test_command_execution(self):
		'''
		A command added successfully is executable
		'''
		# Given a command added to the client that will always execute
		user = User("Rosie")
		args = "foo bar baz"
		command = DummyCommand("foo", [], {})
		command.execute = MagicMock()
		client = CommandClientBase()
		client.commands = {'foo': command}

		# When something that doesn't exist is executed
		result = client.execute('idontexist', user, None)

		# Then nothing happens and a FAILURE is returned
		self.assertEqual(State.FAILURE, result.state)
		command.execute.assert_not_called()

		# When something that does exist is executed
		result = client.execute('foo', user, args)

		# Then it is executed and a SUCCESS is returned
		self.assertEqual(State.SUCCESS, result.state)
		command.execute.assert_called_with(user, "foo bar baz")

	def test_command_disable_enable(self):
		'''
		Commands can be disabled/enabled during runtime and won't be available to execute
		'''
		# Given a client with a command in it
		user = User("Rosie")
		args = "foo bar baz"
		command = DummyCommand("foo", [], {}, "", ["bar", "baz"])
		command.execute = MagicMock()
		client = CommandClientBase()
		client.commands = {'foo': command, 'bar': command, 'baz': command}

		# And that command can be executed normally
		result = client.execute('foo', user, args)
		self.assertEqual(State.SUCCESS, result.state)
		command.execute.assert_called_with(user, "foo bar baz")

		# When a nonexistent command is disabled or enabled then a FAILURE is returned 
		result = client.disable('idontexist')
		self.assertEqual(State.FAILURE, result.state)
		result = client.enable('idontexist')
		self.assertEqual(State.FAILURE, result.state)

		# And the existing command can still be executed
		result = client.execute('foo', user, args)
		self.assertEqual(State.SUCCESS, result.state)
		command.execute.assert_called_with(user, "foo bar baz")

		# When the command is disabled
		result = client.disable('foo')

		# Then the command or any of its aliases cannot be executed
		result = client.execute('foo', user, args)
		self.assertEqual(State.FAILURE, result.state)
		result = client.execute('bar', user, args)
		self.assertEqual(State.FAILURE, result.state)

		# When the command is re-enabled
		result = client.enable('foo')

		# Then the command and its aliases can be executed again
		result = client.execute('foo', user, args)
		self.assertEqual(State.SUCCESS, result.state)
		command.execute.assert_called_with(user, "foo bar baz")

		result = client.execute('bar', user, args)
		self.assertEqual(State.SUCCESS, result.state)
		command.execute.assert_called_with(user, "foo bar baz")

	def test_command_reload(self):
		'''
		Commands can be reloaded during runtime, e.g. if the broadcaster changes 
		something during the broadcast and wants those changes available without
		restarting the entire bot.

		If there is an error, the reload won't happen and a warning will be logged; the 
		bot will still function as normal.
		'''
		# Given a client loaded with commands
		client = CommandClientBase()
		confs = {
			'commands': [
				{
					'name': 'foo',
					'description': '',
					'aliases': ['bar', 'baz'],
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
			]
		}
		client.load_commands(confs)
		self.assertEqual('', client.commands['foo'].description)
		self.assertTrue(isinstance(client.commands['foo'].executor, DummyExecutor))
		self.assertEqual('', client.commands['bar'].description)
		self.assertTrue(isinstance(client.commands['bar'].executor, DummyExecutor))
		self.assertEqual('', client.commands['baz'].description)
		self.assertTrue(isinstance(client.commands['baz'].executor, DummyExecutor))
		
		self.assertEqual(3, len(client.commands))

		# When reloaded with a bad config
		confs['commands'][0]['action']['type'] = "idontexist"
		result = client.reload_commands(confs)

		# Those commands are still in the client, and a FAILURE is returned
		self.assertEqual(State.FAILURE, result.state)
		self.assertEqual('', client.commands['foo'].description)
		self.assertTrue(isinstance(client.commands['foo'].executor, DummyExecutor))
		self.assertEqual('', client.commands['bar'].description)
		self.assertTrue(isinstance(client.commands['bar'].executor, DummyExecutor))
		self.assertEqual('', client.commands['baz'].description)
		self.assertTrue(isinstance(client.commands['baz'].executor, DummyExecutor))
		
		self.assertEqual(3, len(client.commands))

		# When reloaded with a good config
		new_confs = {
			'commands': [
				{
					'name': 'foo',
					'description': 'some description',
					'aliases': ['bar', 'baz'],
					'allows': [
						{
							'type': 'DummyAllow',
							'args': {}
						}
					],
					'action': {
						'type': 'DummyAction',
						'args': {}
					}
				},
				{
					'name': 'beep',
					'description': 'some other description',
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
			]
		}
		client.reload_commands(new_confs)

		# Then the commands are updated and any new commands are added
		self.assertEqual('some description', client.commands['foo'].description)
		self.assertTrue(isinstance(client.commands['foo'].executor, DummyAction))
		self.assertEqual('some description', client.commands['bar'].description)
		self.assertTrue(isinstance(client.commands['bar'].executor, DummyAction))
		self.assertEqual('some description', client.commands['baz'].description)
		self.assertTrue(isinstance(client.commands['baz'].executor, DummyAction))

		self.assertEqual('some other description', client.commands['beep'].description)
		self.assertTrue(isinstance(client.commands['beep'].executor, DummyExecutor))

		self.assertEqual(4, len(client.commands))

		# And finally when reloaded with fewer commands
		new_confs = {
			'commands': [
				{
					'name': 'beep',
					'description': 'some other description',
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
			]
		}
		client.reload_commands(new_confs)

		# Then the old commands are removed
		self.assertEqual(None, client.commands.get('foo', None))
		self.assertEqual(None, client.commands.get('bar', None))
		self.assertEqual(None, client.commands.get('baz', None))

		self.assertEqual('some other description', client.commands['beep'].description)
		self.assertTrue(isinstance(client.commands['beep'].executor, DummyExecutor))

		self.assertEqual(1, len(client.commands))