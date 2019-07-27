import unittest
from unittest.mock import *
from bot import *
import bot.context.ObsContext
import bot.context.CommandContext as ctx
from pathlib import Path
import time

class TestObsClient(unittest.TestCase):

	def setUp(self):
		pass

	def test_obs_actions(self):
		self._do_cmd('showsource', User('foo'), None)
		#self._do_cmd('hidesource', User('foo'), None)

	def _do_cmd(self, command_name, user, args):
		'''
		Give the hooman a somewhat relaxed pace for observing results in OBS
		'''
		print("\nWATCH OBS FOR: {} ({})...".format(command_name, ctx.command_client.commands[command_name].description))
		time.sleep(3)
		self._countdown(3)
		ctx.command_client.execute(command_name, user, args)
		time.sleep(0.75)
		print("...complete!\n")

	def _countdown(self, seconds):
		while(seconds > 0):
			print(seconds)
			time.sleep(1)
			seconds += -1