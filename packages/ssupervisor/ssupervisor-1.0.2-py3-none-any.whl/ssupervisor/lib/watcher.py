import sys
import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from .process import Process

class EventHandler:
	'''
	@about:
		A specific class used by Watchdog which implements explicit
		event handler functions for certain actions.
	@info:
		https://pythonhosted.org/watchdog/api.html#watchdog.events.FileSystemEventHandler
	'''
	def __init__(self, logger, config, pass_arg):
		self.logger = logger
		self.process = Process(self.logger)
		self.config = config
		self.pass_arg = pass_arg
		self.map = {
			'created': self.on_created,
			'deleted': self.on_deleted,
			'modified': self.on_modified,
			'moved': self.on_moved,
		}
	
	def _get_argument(self, event):
		# If invoked with -p or --pass, this will
		# return a string containing:
		# [script/command to run] [path of changed file]
		# If not invoked with -p, this will return only
		# the script/command to run.
		if self.pass_arg:
			return f'{self.config[2]} {event.src_path}'
		return self.config[2]

	def _run_process(self, event, event_type):
		# Performs the script/command and logs it.
		self.logger.log(f'{event_type}: [bold magenta]{event.src_path}[/bold magenta]')
		self.process(self._get_argument(event))

	def dispatch(self, event):
		# Special method for determining which event
		# to notice. This will take the first part
		# of the config file line (modified/any/deleted/etc.)
		self.on_any_event(event)
		
		if event.event_type == self.config[0]:
			self.map[event.event_type](event)

	def on_any_event(self, event):
		# If this check wasn't performed, there would be
		# no use in specifying which type of event to watch.
		# This method is run every time there is a change in
		# the folder.
		if self.config[0] == "any":
			self._run_process(event, event.event_type.capitalize())
	
	# The following 4 methods are specific
	# to Watchdog
	def on_created(self, event):
		self._run_process(event, 'Created')
	
	def on_deleted(self, event):
		self._run_process(event, 'Deleted')
	
	def on_modified(self, event):
		self._run_process(event, 'Modified')
	
	def on_moved(self, event):
		self._run_process(event, 'Moved')

class Watcher:
	def __init__(self, logger):
		self.config = None
		self.logger = logger
		self.pass_arg = False

		self.recursive = None
		self.log = None

	def pass_argument(self):
		# This method is called if Supervisor is
		# invoked with -p or --pass
		self.pass_arg = True

	def _alert(self, config):
		# Explicitly informs the user about the current
		# Watcher configuration.
		self.logger.log(f'\nEvent type: [bold magenta]{config[0]}[/bold magenta]')
		self.logger.log(f'Directory: [bold cyan]{config[1]}[/bold cyan]')
		self.logger.log(f'Operation: [bold green]{config[2]}[/bold green]\n')
		self.logger.log('----------\n')

	def _check_config(self):
		for config in self.config:
			path = config[1][:-1] if config[1].endswith('/') else config[1]
			if path == str(Path.home()) and self.log:
				print('\n'.join([
					'Watching your home directory with logging enabled is not supported.',
					'This would create an infinite loop.',
					'Either disable logging or stop watching your home directory.'
				]))
				quit()

	def _watch(self, configs):
		self._check_config()

		# The main process. The config is simply the middle
		# section of a config file line.
		observers = []
		for config in configs:
			self._alert(config)

			observer = Observer()
			observer.schedule(EventHandler(self.logger, config, self.pass_arg), config[1], recursive=self.recursive)
			observer.start()
			observers.append(observer)
		try:
			while True:
				time.sleep(1) # this will cause Ctrl+C to have a delay
		except KeyboardInterrupt:
			# Instead of this exception, we could watch stdin
			# and then begin another watcher process, if applicable.
			for observer in observers:
				observer.stop()
				observer.join()

	def __call__(self, parsed_config, settings):
		self.config = parsed_config
		self.recursive = settings.get('recursive')
		self.log = settings.get('log')
		self._watch(self.config)