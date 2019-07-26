import unittest
from unittest.mock import *
from bot import *

class TestExecutors(unittest.TestCase):

	def setUp(self):
		pass

	def test_minimum_config(self):
		# Given a minimum configuration 
		# Then an Executor can be instantiated
		try:
			ExecutorBase(**{'args': {"actions": []}})
		except Exception:
			self.fail("Unexpected exception")

		# But given missing information
		# Then a ValueError is thrown
		self.assertRaises(ValueError, ExecutorBase, **{})
		self.assertRaises(ValueError, ExecutorBase, **{'args': {}})

	def test_builds_children_actions_or_executors(self):
		# Given a config that includes children
		config = {
			"args": {
				"actions": [
					{
						"type": "ActionBase",
						"args": {
							"lvl": "a",
							"num": 1
						}
					}, 
					{
						"type": "ExecutorBase",
						"args": {
							"actions": [
								{
									"type": "ExecutorBase",
									"args": {
										"actions": [
											{
												"type": "ActionBase",
												"args": {
													"lvl": "c",
													"num": 1
												}
											}
										]
									}
								},
								{
									"type": "ActionBase",
									"args": {
										"lvl": "b",
										"num": 1
									}
								},
								{
									"type": "ActionBase",
									"args": {
										"lvl": "b",
										"num": 2
									}
								}
							]
						}
					},
					{
						"type": "ActionBase",
						"args": {
							"lvl": "a",
							"num": 2
						}
					}
				]
			}
		}

		# Then when built
		e = ExecutorBase(**config)
		#print(e)

		# The children are built
		self.assertTrue(isinstance(e.actions[0], ActionBase))
		self.assertDictEqual({"lvl": "a", "num": 1}, e.actions[0].args)

		self.assertTrue(isinstance(e.actions[1], ExecutorBase))

		self.assertTrue(isinstance(e.actions[1].actions[0], ExecutorBase))

		self.assertDictEqual({"lvl": "c", "num": 1}, e.actions[1].actions[0].actions[0].args)
		self.assertTrue(isinstance(e.actions[1].actions[0].actions[0], ActionBase))

		self.assertDictEqual({"lvl": "b", "num": 1}, e.actions[1].actions[1].args)
		self.assertTrue(isinstance(e.actions[1].actions[1], ActionBase))

		self.assertTrue(isinstance(e.actions[2], ActionBase))
		self.assertDictEqual({"lvl": "a", "num": 2}, e.actions[2].args)

	def test_all_executor_success(self):
		'''
		Default executor is to execute all Actions in order per request
		'''
		# Given an ExecuteAll Executor and a list of succeeding Actions
		config = {
			"args": {
				"actions": [
					{"type": "DummyAction", "args": {}},
					{"type": "ExecuteAll", "args": {
						"actions": [
							{"type": "DummyAction", "args": {}},
							{"type": "DummyAction", "args": {}}
						]
					}},
					{"type": "DummyAction", "args": {}}
				]
			}
		}

		executor = ExecuteAll(**config)

		a1 =  executor.actions[0]
		a21 = executor.actions[1].actions[0]
		a22 = executor.actions[1].actions[1]
		a3 =  executor.actions[2]
		a1.execute =  MagicMock(return_value=Result(State.SUCCESS))
		a21.execute = MagicMock(return_value=Result(State.SUCCESS))
		a22.execute = MagicMock(return_value=Result(State.SUCCESS))
		a3.execute =  MagicMock(return_value=Result(State.SUCCESS))

		# When executed 
		result = executor.execute(User("foo"), None)

		# Then each action is executed in order
		a1.execute.assert_called_once()
		a21.execute.assert_called_once()
		a22.execute.assert_called_once()
		a3.execute.assert_called_once()

		# And when all execute then a SUCCESS is returned
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(3, len(result.messages))
		self.assertEqual(2, len(result.messages[1].messages))

	def test_all_executor_failure(self):
		'''
		Default executor is to execute all Actions in order per request
		'''
		# Given an ExecuteAll Executor and a list of Actions including a failure
		config = {
			"args": {
				"actions": [
					{"type": "DummyAction", "args": {}},
					{"type": "ExecuteAll", "args": {
						"actions": [
							{"type": "DummyAction", "args": {}},
							{"type": "DummyAction", "args": {}}
						]
					}},
					{"type": "DummyAction", "args": {}}
				]
			}
		}

		executor = ExecuteAll(**config)

		a1 =  executor.actions[0]
		a21 = executor.actions[1].actions[0]
		a22 = executor.actions[1].actions[1]
		a3 =  executor.actions[2]
		a1.execute =  MagicMock(return_value=Result(State.SUCCESS))
		a21.execute = MagicMock(return_value=Result(State.FAILURE))
		a22.execute = MagicMock(return_value=Result(State.SUCCESS))
		a3.execute =  MagicMock(return_value=Result(State.SUCCESS))

		# When executed 
		result = executor.execute(User("foo"), None)

		# Then each action is executed in order
		a1.execute.assert_called_once()
		a21.execute.assert_called_once()
		a22.execute.assert_not_called()
		a3.execute.assert_not_called()

		# And when all execute then a SUCCESS is returned
		self.assertEqual(State.FAILURE, result.state)
		self.assertEqual(2, len(result.messages))
		self.assertEqual(1, len(result.messages[1].messages))

	def test_gated_executor_success(self):
		'''
		Gated executor executes one action per request, only advancing to the 
		next action at the next request if the prior action executed with SUCCESS
		'''
		# Given the Gated Executor and a list of succeeding actions
		config = {
			"args": {
				"actions": [
					{"type": "DummyAction", "args": {}},
					{"type": "ExecuteGated", "args": {
						"actions": [
							{"type": "DummyAction", "args": {}},
							{"type": "DummyAction", "args": {}}
						]
					}},
					{"type": "DummyAction", "args": {}}
				]
			}
		}

		executor = ExecuteGated(**config)

		a1 =  executor.actions[0]
		a21 = executor.actions[1].actions[0]
		a22 = executor.actions[1].actions[1]
		a3 =  executor.actions[2]
		a1.execute =  MagicMock(return_value=Result(State.SUCCESS))
		a21.execute = MagicMock(return_value=Result(State.SUCCESS))
		a22.execute = MagicMock(return_value=Result(State.SUCCESS))
		a3.execute =  MagicMock(return_value=Result(State.SUCCESS))

		# When executed only the next action in the list is executed
		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(0, a21.execute.call_count)
		self.assertEqual(0, a22.execute.call_count)
		self.assertEqual(0, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(1, a21.execute.call_count)
		self.assertEqual(0, a22.execute.call_count)
		self.assertEqual(0, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(1, a21.execute.call_count)
		self.assertEqual(1, a22.execute.call_count)
		self.assertEqual(0, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(1, a21.execute.call_count)
		self.assertEqual(1, a22.execute.call_count)
		self.assertEqual(1, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		# And this same order is maintained when it cycles through the actions again
		result = executor.execute(User("foo"), None)
		self.assertEqual(2, a1.execute.call_count)
		self.assertEqual(1, a21.execute.call_count)
		self.assertEqual(1, a22.execute.call_count)
		self.assertEqual(1, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(2, a1.execute.call_count)
		self.assertEqual(2, a21.execute.call_count)
		self.assertEqual(1, a22.execute.call_count)
		self.assertEqual(1, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(2, a1.execute.call_count)
		self.assertEqual(2, a21.execute.call_count)
		self.assertEqual(2, a22.execute.call_count)
		self.assertEqual(1, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(2, a1.execute.call_count)
		self.assertEqual(2, a21.execute.call_count)
		self.assertEqual(2, a22.execute.call_count)
		self.assertEqual(2, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

	def test_gated_executor_failure(self):
		'''
		Gated executor executes one action per request, only advancing to the 
		next action at the next request if the prior action executed with SUCCESS
		'''
		# Given the Gated Executor and a list of succeeding actions
		config = {
			"args": {
				"actions": [
					{"type": "DummyAction", "args": {}},
					{"type": "ExecuteGated", "args": {
						"actions": [
							{"type": "DummyAction", "args": {}},
							{"type": "DummyAction", "args": {}}
						]
					}},
					{"type": "DummyAction", "args": {}}
				]
			}
		}

		executor = ExecuteGated(**config)

		a1 =  executor.actions[0]
		a21 = executor.actions[1].actions[0]
		a22 = executor.actions[1].actions[1]
		a3 =  executor.actions[2]
		a1.execute =  MagicMock(return_value=Result(State.SUCCESS))
		a21.execute = MagicMock(return_value=Result(State.FAILURE))
		a22.execute = MagicMock(return_value=Result(State.SUCCESS))
		a3.execute =  MagicMock(return_value=Result(State.SUCCESS))

		# When executed only the next action in the list is executed
		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(0, a21.execute.call_count)
		self.assertEqual(0, a22.execute.call_count)
		self.assertEqual(0, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		# When when the next executor in the list fails then it doesn't advance

		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(1, a21.execute.call_count)
		self.assertEqual(0, a22.execute.call_count)
		self.assertEqual(0, a3.execute.call_count)
		self.assertEqual(State.FAILURE, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(2, a21.execute.call_count)
		self.assertEqual(0, a22.execute.call_count)
		self.assertEqual(0, a3.execute.call_count)
		self.assertEqual(State.FAILURE, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(3, a21.execute.call_count)
		self.assertEqual(0, a22.execute.call_count)
		self.assertEqual(0, a3.execute.call_count)
		self.assertEqual(State.FAILURE, result.state)
		self.assertEqual(1, len(result.messages))

		# etc.
		# And when the next item succeeds
		a21.execute = MagicMock(return_value=Result(State.SUCCESS))

		# Then execution order resumes
		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(1, a21.execute.call_count) # Note the count was reset due to changing the Mock above
		self.assertEqual(0, a22.execute.call_count)
		self.assertEqual(0, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(1, a21.execute.call_count)
		self.assertEqual(1, a22.execute.call_count)
		self.assertEqual(0, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(1, a21.execute.call_count)
		self.assertEqual(1, a22.execute.call_count)
		self.assertEqual(1, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		# etc cycling back
		result = executor.execute(User("foo"), None)
		self.assertEqual(2, a1.execute.call_count)
		self.assertEqual(1, a21.execute.call_count)
		self.assertEqual(1, a22.execute.call_count)
		self.assertEqual(1, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(2, a1.execute.call_count)
		self.assertEqual(2, a21.execute.call_count)
		self.assertEqual(1, a22.execute.call_count)
		self.assertEqual(1, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(2, a1.execute.call_count)
		self.assertEqual(2, a21.execute.call_count)
		self.assertEqual(2, a22.execute.call_count)
		self.assertEqual(1, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(2, a1.execute.call_count)
		self.assertEqual(2, a21.execute.call_count)
		self.assertEqual(2, a22.execute.call_count)
		self.assertEqual(2, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

if __name__ == '__main__':
	unittest.main()