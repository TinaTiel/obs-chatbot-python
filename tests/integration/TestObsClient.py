import unittest
import bot.context.ObsContext as obs_ctx
import bot.context.CommandContext as cmd_ctx
from bot.User import User
from pathlib import Path
import time

class TestObsClient(unittest.TestCase):

	def setUp(self):
		pass

	def test_obs_actions(self):
		obs_ctx.obs_client.connect()
		self._do_cmd('showsource', User('foo'), None)
		#self._do_cmd('hidesource', User('foo'), None)

	def _do_cmd(self, command_name, user, args):
		'''
		Give the hooman a somewhat relaxed pace for observing results in OBS
		'''
		print("\nWATCH OBS FOR: {} ({})...".format(command_name, cmd_ctx.command_client.commands[command_name].description))
		time.sleep(3)
		self._countdown(3)
		cmd_ctx.command_client.execute(command_name, user, args)
		time.sleep(0.75)
		print("...complete!\n")

	def _countdown(self, seconds):
		while(seconds > 0):
			print(seconds)
			time.sleep(1)
			seconds += -1