from pathlib import Path
from utils import Logger
import json

class LurkBot:
	def __init__(self, config):
		print('yay')
		input('')

def Main():
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
		config['settings'] = '[]'
		# Set keywords to get pinged for.
		config['keywords'] = config['channel']

		# Save our settings in a config file.
		open('./config/config.json', 'w').write(json.dumps(config))
	
	# Start the bot
	lurkbot = LurkBot(open('./config/config.json', 'r').read())

Main()