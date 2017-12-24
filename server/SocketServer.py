# Script that handles the socket server
# pip install git+https://github.com/dpallot/simple-websocket-server.git

from SimpleWebSocketServer import WebSocket
from utils import Logger
import json

lurkbot = None
clients = []

class SocketServer(WebSocket):
	def handleMessage(self):
		try:
			data = json.loads(self.data)
			Logger.writeLine('[SOCKET] [MSG] ' + self.data)

			if 'auth' in data:
				if data['auth'] == lurkbot.passwd:
					clients.append(self)
					# Send a message to the client.
					dump = json.dumps({'auth': 'success'})

					self.sendMessage(dump)
					Logger.writeLine('[SOCKET] [SEND] ' + dump)
				else:
					# Send a message to the client.
					dump = json.dumps({'auth': 'failed'})

					self.sendMessage(dump)

					Logger.writeLine('[SOCKET] [SEND] ' + dump)
					# Close the connection.
					self.close()
		except Exception as e:
			Logger.errorLine('[SOCKET] [' + self.data + '] ' + str(e))

	def handleConnected(self):
		Logger.writeLine('[SOCKET] New connection from: ' + self.address[0])

	def handleClose(self):
		clients.remove(self)

def sendToAll(username, message, channel):
	jsonDump = json.dumps({'sender': username, 'channel': channel, 'message': message})

	for client in clients:
		Logger.writeLine('[SOCKET] [SEND] ' + jsonDump)
		client.sendMessage(jsonDump)

def setLurkBot(obj):
	global lurkbot

	lurkbot = obj