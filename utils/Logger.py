import datetime

debug = False

def writeLine(message):
	print('[' + datetime.datetime.now().strftime('%Y-%m-%d @ %I:%M:%S.%f') + ']', message)

def errorLine(message):
	print('[' + datetime.datetime.now().strftime('%Y-%m-%d @ %I:%M:%S.%f') + '] [ERROR]', message)

def debugLine(message):
	if (debug):
		print('[' + datetime.datetime.now().strftime('%Y-%m-%d @ %I:%M:%S.%f') + '] [DEBUG]', message)

def setDebug(toggle):
	debug = toggle