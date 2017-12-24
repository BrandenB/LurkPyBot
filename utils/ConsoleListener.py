# Listener that keeps the console alive.

from threading import Thread
from time import sleep
from utils import Logger
import sys

class ConsoleListener(Thread):
	def __init__(self):
		super().__init__()
		self.killed = False

	def run(self):
		while not self.killed:
			try:
				line = input()

				if (line == 'exit'):
					sys.exit(1)

				sleep(0.02)
			except Exception as ex:
				Logger.debugLine(ex)

	def kill(self):
		self.killed = True
