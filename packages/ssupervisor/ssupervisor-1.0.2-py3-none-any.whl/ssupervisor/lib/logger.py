from pathlib import Path
from rich.console import Console

class Logger:
	def __init__(self):
		self.output_file = f'{Path.home()}/supervisor.log'
		self.should_output = False
		self.console = Console()
	
	def log_to_file(self, message):
		if self.should_output:
			with open(self.output_file, 'a') as out_f:
				out_f.write(f'\n{message}')

	def log(self, message):
		self.console.print(message)
		self.log_to_file(message)