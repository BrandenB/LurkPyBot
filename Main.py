# Main script where everything starts.

from SimpleWebSocketServer import SimpleWebSocketServer
from pathlib import Path
from utils import Logger
from utils import ConsoleListener
from twitch import Connection
from server import SocketServer
import threading
import atexit
import json
import re

lurkbot = None
listener = None
class LurkBot:
	def __init__(self, config, listener):
		self.username = config['username']
		self.channel = config['channel']
		self.oauth = config['oauth']
		self.passwd = config['pass']
		self.ip = config['IP']
		self.port = config['PORT']
		self.settings = {}
		self.keywords = []
		self.listener = listener
		self.config = config

		# Save channel settings.
		settings = config['settings']
		for setting in settings:
			self.settings[setting['channel']] = setting

		# Save keywords.
		keywords = config['keywords'].split(',')
		for keyword in keywords:
			self.keywords.append(re.compile('\\b' + keyword + '\\b'))

		# Create a new connection.
		self.connection = Connection.Connection('wss://irc-ws.chat.twitch.tv')
		# Give this object to the connection class
		self.connection.init(self)
		# Connect.
		self.connection.connect()
		# Create a new socket server.
		self.server = SimpleWebSocketServer(self.ip, int(self.port), SocketServer.SocketServer)
		# Create a new thread for the socket server
		self.serverThread = threading.Thread(target=self.server.serveforever)
		# Make the thread daemon
		self.serverThread.setDaemon(True)
		# Set the lurkbot object
		SocketServer.setLurkBot(self)
		# Start the thread.
		self.serverThread.start()

def Main():
	# Register our exit hook.
	atexit.register(onExit)

	if (not Path('./config/config.json').is_file()):
		config = {}

		# Ask for the username.
		print('Please enter your username : ', end='')
		config['username'] = input().lower()

		# Ask for the channel name.
		print('Please enter the channel name you want to join : ', end='')
		config['channel'] = input().lower()

		# Ask for the oauth token.
		print('Please enter your oauth token : ', end='')
		config['oauth'] = input()

		# Ask for password for the events socket.
		print('Please enter a custom password for the event socket : ', end='')
		config['pass'] = input()

		# Ask for an IP for the events socket.
		print('Please enter your server IP address : ', end='')
		config['IP'] = input()

		# Ask for a PORT for the events socket.
		print('Please enter a port for the socket : ', end='')
		config['PORT'] = input()

		# Set an empty array for settings.
		config['settings'] = []
		# Set keywords to get pinged for.
		config['keywords'] = config['channel']

		# Save our settings in a config file.
		open('./config/config.json', 'w').write(json.dumps(config))
	
	# Print bot details.
	Logger.writeLine('')
	Logger.writeLine('LurkBot Version: 3.0')
	Logger.writeLine('Creator: ScaniaTV')
	Logger.writeLine('')

	# Start the console listener.
	global listener
	listener = ConsoleListener.ConsoleListener()
	listener.start()

	# Start the bot.
	global lurkbot
	lurkbot = LurkBot(json.loads(open('./config/config.json', 'r').read()), listener)

def onExit():
	Logger.writeLine('Socket server closing since the thread is daemon...')

	if (lurkbot != None):
		Logger.writeLine('Closing connection with Twitch...')
		lurkbot.connection.close()

	if (listener != None):
		Logger.writeLine('Terminating console listener...')
		listener.kill()

	Logger.writeLine('Bye.')

Main()
