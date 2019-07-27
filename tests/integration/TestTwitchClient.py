import unittest
from unittest.mock import *
from bot import *
import bot.context.AppContext
import bot.context.TwitchContext as ctx
from pathlib import Path

class TestTwitchClient(unittest.TestCase):

	def setUp(self):
		pass

	def test_something(self):
		'''
		Initializing the app and Twitch context does all we need this to do
		Just verify with !twitchstatus that the bot responds.
		'''
		pass