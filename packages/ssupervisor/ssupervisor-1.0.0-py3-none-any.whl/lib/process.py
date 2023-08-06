import subprocess

class Process:
	def __init__(self, logger = None):
		self.logger = logger
		self.process = None

	def _run(self):
		subprocess.run(self.process.split())
		self.logger.log(f'Executed: [bold green]{self.process}[/bold green]')
	
	def __call__(self, process):
		self.process = process
		self._run()