import unittest
import sys

import os.path
from os import path

sys.path.append('../')
import bot

class TestBot(unittest.TestCase):

	def testCreateMessage(self):
		msg = bot.create_satine_reply_message()
		self.assertIsNotNone(msg, 'Reply message is None')

	def testConfigFileExists(self):
		exists = path.exists('../bot.cfg')
		self.assertTrue(exists, 'Config file does not exist')

if __name__ == '__main__':
	unittest.main()