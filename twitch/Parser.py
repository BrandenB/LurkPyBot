# Script that parses messages from Twitch and sends the event to the event handler.

from utils import Logger

def parse(lurkbot, connection, eventHandler, rawMessage):
	try:
		messageParts = str(rawMessage).split(' :', 3)
		username = ''
		message = ''
		event = ''
		tags = {}

		# Get our tags.
		if (messageParts[0].startswith('@')):
			# Split our tags.
			tagArray = messageParts[0][1:].split(';')
			# Loop our tags.
			for i in range(len(tagArray)):
				tag = tagArray[i].split('=')
				if (len(tag) > 0):
					tags[tag[0]] = '' if len(tag) < 2 else tag[1]

			messageParts[0] = messageParts[1]
			if (len(messageParts) > 2):
				messageParts[1] = messageParts[2]

		# Get the message.
		if len(messageParts) > 1:
			if (messageParts[1].startswith(' ')):
				messageParts[1] = messageParts[1][1:]
			message = messageParts[1]
			if len(message) > 1:
				message = message[0:len(message) - 1]

		# Get the username.
		if messageParts[0].find('!') != -1:
			username = messageParts[0][messageParts[0].index('!') + 1:messageParts[0].index('@')]

		# Get the event.
		event = '' if messageParts[0].find(' ') == -1 else messageParts[0].split(' ')[1]

		if (event == 'PRIVMSG'):
			Logger.writeLine(username + ': ' + message)
		elif (event == '001'):
			connection.send('JOIN #sodapoppin')
	except Exception as ex:
		Logger.errorLine('Failed to parse a message from Twitch-IRC: ' + ex)
