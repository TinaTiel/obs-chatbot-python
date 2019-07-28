import unittest
import bot.context.ObsContext
import bot.context.TwitchContext
import bot.context.CommandContext as ctx
from bot.User import User
from pathlib import Path

class TestAll(unittest.TestCase):

	def setUp(self):
		pass

	def test_all(self):
		ctx.twitch_client.obs_client = ctx.obs_client