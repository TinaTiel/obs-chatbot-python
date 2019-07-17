import unittest
from unittest.mock import *
from bot import *

class TestExecutors(unittest.TestCase):

	def setUp(self):
		pass

	def test_default_executor_success(self):
		'''
		Default executor is to execute all Actions in order per request
		'''
		# Given the default Executor and a list of Actions
		a1 = Action()
		a2 = Action()
		a3 = Action()
		a1.execute = MagicMock(return_value=Result(State.SUCCESS))
		a2.execute = MagicMock(return_value=Result(State.SUCCESS))
		a3.execute = MagicMock(return_value=Result(State.SUCCESS))
		executor = Executor([a1, a2, a3])

		# When executed 
		result = executor.execute(User("foo"), None)

		# Then each action is executed in order
		a1.execute.assert_called_once()
		a2.execute.assert_called_once()
		a3.execute.assert_called_once()

		# And when all execute then a SUCCESS is returned
		self.assertEqual(State.SUCCESS, result.state)
		self.assertEqual(3, len(result.messages))

	def test_default_executor_failure(self):
		'''
		Default executor is to execute all Actions in order per request
		'''
		# Given the default Executor and a list of Actions
		a1 = Action()
		a2 = Action()
		a3 = Action()
		a1.execute = MagicMock(return_value=Result(State.SUCCESS))
		a2.execute = MagicMock(return_value=Result(State.FAILURE))
		a3.execute = MagicMock(return_value=Result(State.SUCCESS))
		executor = Executor([a1, a2, a3])

		# When executed 
		result = executor.execute(User("foo"), None)

		# Then each action is executed in order
		a1.execute.assert_called_once()
		a2.execute.assert_called_once()
		a3.execute.assert_not_called()

		# And when all execute then a SUCCESS is returned
		self.assertEqual(State.FAILURE, result.state)
		self.assertEqual(2, len(result.messages))

	def test_gated_executor(self):
		'''
		Gated executor executes one action per request, only advancing to the 
		next action at the next request if the prior action executed with SUCCESS
		'''
		pass

if __name__ == '__main__':
	unittest.main()