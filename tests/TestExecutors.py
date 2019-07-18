import unittest
from unittest.mock import *
from bot import *

class TestExecutors(unittest.TestCase):

	def setUp(self):
		pass

	def test_all_executor_success(self):
		'''
		Default executor is to execute all Actions in order per request
		'''
		# Given the default Executor and a list of succeeding Actions
		a1 = Action(**{"args": {}})
		a2 = Action(**{"args": {}})
		a3 = Action(**{"args": {}})
		a1.execute = MagicMock(return_value=Result(State.SUCCESS))
		a2.execute = MagicMock(return_value=Result(State.SUCCESS))
		a3.execute = MagicMock(return_value=Result(State.SUCCESS))
		executor = ExecuteAll(**{"actions": [a1, a2, a3]})

		# When executed 
		result = executor.execute(User("foo"), None)

		# Then each action is executed in order
		a1.execute.assert_called_once()
		a2.execute.assert_called_once()
		a3.execute.assert_called_once()

		# And when all execute then a SUCCESS is returned
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(3, len(result.messages))

	def test_all_executor_failure(self):
		'''
		Default executor is to execute all Actions in order per request
		'''
		# Given the default Executor and a list of Actions including a failure
		a1 = Action(**{"args": {}})
		a2 = Action(**{"args": {}})
		a3 = Action(**{"args": {}})
		a1.execute = MagicMock(return_value=Result(State.SUCCESS))
		a2.execute = MagicMock(return_value=Result(State.FAILURE))
		a3.execute = MagicMock(return_value=Result(State.SUCCESS))
		executor = ExecuteAll(**{"actions": [a1, a2, a3]})

		# When executed 
		result = executor.execute(User("foo"), None)

		# Then each action is executed in order
		a1.execute.assert_called_once()
		a2.execute.assert_called_once()
		a3.execute.assert_not_called()

		# And when all execute then a SUCCESS is returned
		self.assertEqual(State.FAILURE, result.state)
		self.assertEqual(2, len(result.messages))

	def test_gated_executor_success(self):
		'''
		Gated executor executes one action per request, only advancing to the 
		next action at the next request if the prior action executed with SUCCESS
		'''
		# Given the Gated Executor and a list of succeeding actions
		a1 = Action(**{"args": {}})
		a2 = Action(**{"args": {}})
		a3 = Action(**{"args": {}})
		a1.execute = MagicMock(return_value=Result(State.SUCCESS))
		a2.execute = MagicMock(return_value=Result(State.SUCCESS))
		a3.execute = MagicMock(return_value=Result(State.SUCCESS))
		executor = ExecuteGated(**{"actions": [a1, a2, a3]})

		# When executed only the next action in the list is executed
		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(0, a2.execute.call_count)
		self.assertEqual(0, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(1, a2.execute.call_count)
		self.assertEqual(0, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(1, a2.execute.call_count)
		self.assertEqual(1, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		# And this same order is maintained when it cycles through the actions again
		result = executor.execute(User("foo"), None)
		self.assertEqual(2, a1.execute.call_count)
		self.assertEqual(1, a2.execute.call_count)
		self.assertEqual(1, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(2, a1.execute.call_count)
		self.assertEqual(2, a2.execute.call_count)
		self.assertEqual(1, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(2, a1.execute.call_count)
		self.assertEqual(2, a2.execute.call_count)
		self.assertEqual(2, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

	def test_gated_executor_failure(self):
		'''
		Gated executor executes one action per request, only advancing to the 
		next action at the next request if the prior action executed with SUCCESS
		'''
		# Given the Gated Executor and a list of succeeding actions
		a1 = Action(**{"args": {}})
		a2 = Action(**{"args": {}})
		a3 = Action(**{"args": {}})
		a1.execute = MagicMock(return_value=Result(State.SUCCESS))
		a2.execute = MagicMock(return_value=Result(State.FAILURE))
		a3.execute = MagicMock(return_value=Result(State.SUCCESS))
		executor = ExecuteGated(**{"actions": [a1, a2, a3]})

		# When executed only the next action in the list is executed
		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(0, a2.execute.call_count)
		self.assertEqual(0, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		# When when the next executor in the list fails then it doesn't advance
		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(1, a2.execute.call_count)
		self.assertEqual(0, a3.execute.call_count)
		self.assertEqual(State.FAILURE, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(2, a2.execute.call_count)
		self.assertEqual(0, a3.execute.call_count)
		self.assertEqual(State.FAILURE, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(3, a2.execute.call_count)
		self.assertEqual(0, a3.execute.call_count)
		self.assertEqual(State.FAILURE, result.state)
		self.assertEqual(1, len(result.messages))

		# etc.
		# And when the next item succeeds
		a2.execute = MagicMock(return_value=Result(State.SUCCESS))

		# Then execution order resumes
		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(1, a2.execute.call_count)
		self.assertEqual(0, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

		result = executor.execute(User("foo"), None)
		self.assertEqual(1, a1.execute.call_count)
		self.assertEqual(1, a2.execute.call_count)
		self.assertEqual(1, a3.execute.call_count)
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(1, len(result.messages))

	def test_executors_can_contain_executors(self):
		# Given the default Executor and a list of succeeding Actions AND an Executor containing Executors
		a1 = Action(**{"args": {}})
		a2 = Action(**{"args": {}})
		a3 = Action(**{"args": {}})
		a4 = Action(**{"args": {}})
		a5 = Action(**{"args": {}})
		a6 = Action(**{"args": {}})
		a7 = Action(**{"args": {}})
		a1.execute = MagicMock(return_value=Result(State.SUCCESS))
		a2.execute = MagicMock(return_value=Result(State.SUCCESS))
		a3.execute = MagicMock(return_value=Result(State.SUCCESS))
		a4.execute = MagicMock(return_value=Result(State.SUCCESS))
		a5.execute = MagicMock(return_value=Result(State.SUCCESS))
		a6.execute = MagicMock(return_value=Result(State.SUCCESS))
		a7.execute = MagicMock(return_value=Result(State.SUCCESS))
		executor = ExecuteAll(**{"actions":[a1, 
												ExecuteAll(**{"actions":[a2, 
																	a3, 
																	ExecuteAll(**{"actions":[a4, 
																						a5]}),
																	a6]}), 
												a7]}) # etc...

		# When executed 
		result = executor.execute(User("foo"), None)

		# Then each action is executed in order including those contained in an Executor
		a1.execute.assert_called_once()
		a2.execute.assert_called_once()
		a3.execute.assert_called_once()
		a4.execute.assert_called_once()
		a5.execute.assert_called_once()
		a6.execute.assert_called_once()
		a7.execute.assert_called_once()

		# And when all execute then a SUCCESS is returned including for nested executors
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(3, len(result.messages))

		self.assertEqual(State.SUCCESS, result.messages[1].state)
		self.assertEqual(4, len(result.messages[1].messages))

		self.assertEqual(State.SUCCESS, result.messages[1].messages[2].state)
		self.assertEqual(2, len(result.messages[1].messages[2].messages))

if __name__ == '__main__':
	unittest.main()