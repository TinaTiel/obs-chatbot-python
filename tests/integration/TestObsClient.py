import unittest
from unittest.mock import *
from bot import *
import bot.Context as ctx
from pathlib import Path

class TestObsClient(unittest.TestCase):

	def setUp(self):
		pass

	def test_something(self):
		ctx.secrets_obs = Path(ctx.secrets_root, 'obs.example.json')
		ctx