from threading import Thread
from time import sleep

class ConsoleListener(Thread):
	def __init__(self):
		super(ConsoleListener, self).__init__()
		self.killed = False

	def run(self):
		while not self.killed:
			line = input()
			sleep(0.01)

	def kill(self):
		self.killed = True
