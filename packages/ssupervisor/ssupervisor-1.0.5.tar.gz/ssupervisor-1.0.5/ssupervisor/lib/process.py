from os import system

class Process:
	def __init__(self, logger = None):
		self.logger = logger
		self.process = None

	def _run(self):
		system(self.process)
		self.logger.log('Executed', self.process, 'green')
	
	def __call__(self, process):
		self.process = process
		self._run()