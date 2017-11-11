import datetime

def writeLine(message):
	print('[' + datetime.datetime.now().strftime('%Y-%m-%d @ %I:%M:%S.%f') + ']', message)