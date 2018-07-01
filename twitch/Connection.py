# Script that handle the connection with Twitch.
# pip install ws4py

from ws4py.client.threadedclient import WebSocketClient
from utils import Logger
from twitch import Parser
from twitch import EventHandler

class Connection(WebSocketClient):
	def init(self, lurkbot):
		Logger.writeLine('Connecting to Twitch-IRC...')
		self.eventHandler = EventHandler.EventHandler()
		self.lurkbot = lurkbot

	def opened(self):
		Logger.writeLine('Connected to Twitch-IRC as ' + self.lurkbot.username)

		self.send('PASS ' + self.lurkbot.oauth)
		self.send('NICK ' + self.lurkbot.username)

	def closed(self, code, reason):
		if (code != 1000):
			Logger.writeLine('Connection with Twitch-IRC was lost. Trying to reconnect...')
		else:
			Logger.debugLine('Disconnected from Twitch-IRC.')
		
		# Try to connect again.
                self.init(self, self.lurkbot)
		self.connect()
		Logger.debugLine('Disconnected: [' + str(code) + '] [' + str(reason) + ']')

	def received_message(self, message):
		message = str(message)

		if (message.startswith('PING')):
			self.sendRaw('PONG :tmi.twitch.tv')
		else:
			Parser.parse(self.lurkbot, self, self.eventHandler, message)

	def sendMessage(self, channel, message):
		Logger.writeLine('[CHAT] [' + channel + '] ' + message)
		self.send('PRIVMSG ' + channel + ' :' + message)

	def sendRaw(self, message):
		Logger.debugLine('[RAW] ' + message)
		self.send(message)
