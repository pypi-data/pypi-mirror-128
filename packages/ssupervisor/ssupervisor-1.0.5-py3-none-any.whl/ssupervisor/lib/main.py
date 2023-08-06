import sys
import time

from .config import Config
from .parser import Parser
from .logger import Logger
from .watcher import Watcher

class Supervisor:
	def __init__(self, settings):
		self.settings = settings

		self.config = Config()
		self.parser = Parser()
		self.logger = Logger()
		self.watcher = Watcher(self.logger)
	
	def _handle_special_arguments(self):
		if self.settings.get('log'):
			self.logger.should_output = True
			self.logger.log_to_file('==========')
				
		if self.settings.get('pass_argument'):
			self.watcher.pass_argument()

	def __call__(self):
		self._handle_special_arguments()
		self.watcher(self.parser.parse(self.config._get_config()), self.settings)