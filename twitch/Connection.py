# Script that handle the connection with Twitch.

from ws4py.client.threadedclient import WebSocketClient
from utils import Logger
from twitch import Parser

class Connection(WebSocketClient):
	def init(self, lurkbot):
		Logger.writeLine('Connecting to Twitch-IRC...')
		self.lurkbot = lurkbot

	def opened(self):
		Logger.writeLine('Connected to Twitch-IRC as ' + self.lurkbot.username)

		self.send('PASS ' + self.lurkbot.passwd)
		self.send('NICK ' + self.lurkbot.username)

	def closed(self, code, reason):
		Logger.writeLine('Connection with Twitch-IRC was lost. Trying to reconnect...')
		Logger.debugLine('Disconnected: [' + code + '] [' + reason + ']')

	def received_message(self, message):
		Parser.parse(self.lurkbot, self, None, message)