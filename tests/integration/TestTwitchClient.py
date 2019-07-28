import unittest
from unittest.mock import *
from bot import *
import bot.context.AppContext
import bot.context.TwitchContext as twitch_ctx
import bot.context.CommandContext as command_ctx
from pathlib import Path

twitch_ctx.twitch_client.command_client = command_ctx.command_client

class TestTwitchClient(unittest.TestCase):

	def setUp(self):
		pass

	def test_something(self):
		'''
		Initializing the app and Twitch context does all we need this to do
		Just verify with !twitchstatus that the bot responds.
		'''
		twitch_ctx.twitch_client.command_client = command_ctx.command_client
		# print(twitch_ctx.bar)
		# twitch_ctx.bar = "baz"
		# print(twitch_ctx.bar)

		twitch_ctx.twitch_client.start()
		twitch_ctx.twitch_client.run_forever()
		