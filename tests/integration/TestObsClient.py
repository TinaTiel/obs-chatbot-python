import unittest
from unittest.mock import *
from bot import *
import bot.context.ObsContext
import bot.context.CommandContext as ctx
from pathlib import Path

class TestObsClient(unittest.TestCase):

	def setUp(self):
		pass

	def test_something(self):
		ctx.command_client.execute("showsource", User("foo"), None)