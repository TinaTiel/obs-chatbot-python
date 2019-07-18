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
			command_manager.build_executor({'type': "ExecuteAll", 'args': {"actions":[]}})
		except ValueError:
			self.fail("command manager build_executor() failed unexpectedly!")

	def test_execute_params_valid_type(self):

		command_manager = CommandManager()

		# Given an invalid type, expect a ValueError
		self.assertRaises(ValueError, command_manager.build_executor, {"type": "asdfasdfasdfasdfasdfasdf", "args": {}})
		self.assertRaises(ValueError, command_manager.build_executor, {"type": "Action", "args": {}})

		# Otherwise given a valid type (from the Executor module), no errors
		try:
			command_manager.build_executor({"type": "ExecuteAll", "args": {"actions":[]}})
			command_manager.build_executor({"type": "ExecuteGated", "args": {"actions":[]}})
		except ValueError:
			self.fail("command manager build_executor() failed unexpectedly")

	def test_action_params(self):
		# type and args are required
		command_manager = CommandManager()
		self.assertRaises(ValueError, command_manager.build_action, {})
		self.assertRaises(ValueError, command_manager.build_action, {"type": "Action"})
		self.assertRaises(ValueError, command_manager.build_action, {"args": {}})

		# Otherwise if all are required
		# No errors occur
		try:
			command_manager.build_action({'type': "Action", 'args': {'args': {} }})
		except ValueError:
			self.fail("command manager build_action() failed unexpectedly!")

	def test_action_params_valid_type(self):

		command_manager = CommandManager()

		# Given an invalid type, expect a ValueError
		self.assertRaises(ValueError, command_manager.build_executor, {"type": "asdfasdfasdfasdfasdfasdf", "args": {}})

		# Otherwise given a valid type (from the Action module), no errors
		try:
			command_manager.build_action({"type": "Action", "args": {'args': {} }})
		except ValueError:
			self.fail("command manager build_action() failed unexpectedly")

	def test_full_command(self):
		# Given a full configuration with nested commands
		conf = {
			"name": "foo",
			"description": "foo description", 
			"aliases": ["bar", "baz", "chirp"],
			"allows": [
				{
					"type": "AllowUserStatus",
					"args": {
						"min_status": "EVERYONE"
					}
				},
				{
					"type": "AllowVoting",
					"args": {
						"min_votes": 5
					}
				}
			],
			"execute": {
				"type": "ExecuteAll",
				"args": {
					"actions": [
						{
							"type": "AnyArgs",
							"args": {
								"lvl": "a",
								"num": 1
							}
						}, 
						{
							"type": "ExecuteGated",
							"args": {
								"actions": [
									{
										"type": "ExecuteAll",
										"args": {
											"actions": [
												{
													"type": "AnyArgs",
													"args": {
														"lvl": "c",
														"num": 1
													}
												}
											]
										}
									},
									{
										"type": "AnyArgs",
										"args": {
											"lvl": "b",
											"num": 1
										}
									},
									{
										"type": "AnyArgs",
										"args": {
											"lvl": "b",
											"num": 2
										}
									}
								]
							}
						},
						{
							"type": "AnyArgs",
							"args": {
								"lvl": "a",
								"num": 2
							}
						}
					]
				}
			}
		}

		# When built
		command_manager = CommandManager()
		cmd = command_manager.build_command(conf)

		# It has all the properties we expect
		self.assertEquals("foo", cmd.name)
		self.assertEquals("foo description", cmd.description)
		self.assertSequenceEqual(["bar", "baz", "chirp"], cmd.aliases)
		self.assertTrue(isinstance(cmd.allows[0], AllowUserStatus))
		self.assertTrue(isinstance(cmd.allows[1], AllowVoting))
		self.assertTrue(isinstance(cmd.executor, ExecuteAll))
		self.assertDictEqual({"lvl": "a", "num": 1}, cmd.executor.actions[0].args)
		self.assertTrue(isinstance(cmd.executor.actions[1], ExecuteGated))
		self.assertTrue(isinstance(cmd.executor.actions[1].actions[0], ExecuteAll))
		self.assertDictEqual({"lvl": "c", "num": 1}, cmd.executor.actions[1].actions[0].actions[0].args)
		self.assertDictEqual({"lvl": "b", "num": 1}, cmd.executor.actions[1].actions[1].args)
		self.assertDictEqual({"lvl": "a", "num": 2}, cmd.executor.actions[2].args)

		def test_command_registry_and_retrieval(self):
			pass

if __name__ == '__main__':
	unittest.main()