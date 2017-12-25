# Script that handle events from Twitch
from server import SocketServer
from utils import Logger
from time import sleep
import re

class EventHandler:
	def _001(self, connection, channels):
		channels = channels.split(',')

		# Request tags.
		connection.sendRaw('CAP REQ :twitch.tv/commands')
		connection.sendRaw('CAP REQ :twitch.tv/tags')

		for channel in channels:
			connection.sendRaw('JOIN #' + channel)
			Logger.writeLine('Joined Channel [#' + channel + ']')

	def _privmsg(self, lurkbot, connection, channel, username, message, tags):
		Logger.writeLine('[PRIVMSG] [' + channel + '] ' + username + ': ' + message)

		# Check if the message has our keyword.
		keywords = lurkbot.keywords
		for keyword in keywords:
			if keyword.match(message):
				SocketServer.sendToAll(username, message, channel)

		# Check for bits.
		if ('bits' in tags) and (channel in lurkbot.settings):
			settings = lurkbot.settings[channel]
			if settings['announce_bits'] == 'true':
				connection.sendMessage(channel, settings["bits_welcome_message"].replace('%NAME%', username).replace('%BITS%', tags['bits']))

	def _whisper(self, lurkbot, connection, channel, username, message, tags):
		Logger.writeLine('[WHISPER] ' + username + ': ' + message)

	def _roomstate(self, lurkbot, connection, channel, username, message, tags):
		Logger.debugLine('[ROOMSTATE] [' + channel + '] [' + username + '] ' + str(tags))

	def _userstate(self, lurkbot, connection, channel, username, message, tags):
		Logger.debugLine('[USERSTATE] [' + channel + '] ' + ('user' if len(tags['user-type']) == 0 else tags['user-type']))

	def _usernotice(self, lurkbot, connection, channel, username, message, tags):
		Logger.writeLine('[USERNOTICE] [' + channel + '] [' + tags['msg-id'] + '/' + tags['msg-param-sub-plan'] + '] ' + tags['login'])

		if channel in lurkbot.settings:
			settings = lurkbot.settings[channel]

			if tags['msg-id'] == 'sub':
				if tags['msg-param-sub-plan'] == 'Prime':
					if settings['announce_prime_subscribers'] == 'true':
						connection.sendMessage(channel, settings['prime_subscibers_welcome_message'].replace('%NAME%', tags['login']))
				else:
					if settings['announce_subscribers'] == 'true':
						connection.sendMessage(channel, settings['subscibers_welcome_message'].replace('%NAME%', tags['login']))
			elif tags['msg-id'] == 'resub' and settings['announce_re_subscribers'] == 'true':
				connection.sendMessage(channel, settings['re_subscibers_welcome_message'].replace('%NAME%', tags['login']).replace('%MONTHS%', tags['msg-param-months']))
			elif tags['msg-id'] == 'subgift' and settings['announce_subscriber_gifts'] == 'true': 
				connection.sendMessage(channel, settings['subsciber_gift_welcome_message'].replace('%NAME%', tags['login']).replace('%RECIPIENT%', tags['msg-param-recipient-user-name']))

