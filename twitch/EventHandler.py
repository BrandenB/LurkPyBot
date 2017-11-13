# Script that handle events from Twitch

from utils import Logger
from time import sleep

class EventHandler:
	def _001(self, connection, channels):
		channels = channels.split(',')

		# Request tags, with a delay since Twitch can't handle them fast.
		sleep(0.1)
		connection.sendRaw('CAP REQ :twitch.tv/membership')
		sleep(0.02)
		connection.sendRaw('CAP REQ :twitch.tv/tags')
		sleep(0.02)
		connection.sendRaw('CAP REQ :twitch.tv/commands')

		for channel in channels:
			connection.sendRaw('JOIN #' + channel)
			Logger.writeLine('Joined Channel [#' + channel + ']')

	def _privmsg(self, lurkbot, connection, channel, username, message, tags):
		Logger.writeLine('[PRIVMSG] [' + channel + '] ' + username + ': ' + message)

	def _whisper(self, lurkbot, connection, channel, username, message, tags):
		Logger.writeLine('[WHISPER] ' + username + ': ' + message)

	def _roomstate(self, lurkbot, connection, channel, username, message, tags):
		Logger.debugLine('[ROOMSTATE] [' + channel + '] [' + username + '] ' + str(tags) + '')

	def _userstate(self, lurkbot, connection, channel, username, message, tags):
		Logger.writeLine('[USERSTATE] [' + channel + '] ' + ('user' if len(tags['user-type']) == 0 else tags['user-type']))

	def _usernotice(self, lurkbot, connection, channel, username, message, tags):
		Logger.writeLine('[USERNOTICE] [' + channel + '] [' + username + '] ' + str(tags) + '')