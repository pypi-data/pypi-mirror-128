'''
Handles parsing of the .supervisorconf file.
'''

import os

class InvalidEventValue(Exception):
	pass

class InvalidPathValue(Exception):
	pass

class Parser:
	def __init__(self):
		self.config = None
	
	def _verify_event(self, event):
		# Make sure the event values are valid
		events = ['any', 'created', 'modified', 'deleted', 'moved']
		if event not in events:
			raise InvalidEventValue(f'\n\nYou cannot use "{event}" as an event value.\n\nThe available options are: {events}\n')
		
	def _verify_path(self, path):
		# Make sure the requested path exists
		if not os.path.exists(path):
			raise InvalidPathValue(f'The path, "{path}" does not exist.')

	def _verify_values(self, lines):
		# Handles running error-checking parse
		# functions on different parts of a config
		# line.
		for line in lines:
			self._verify_event(line[0])
			self._verify_path(line[1])


	def parse(self, config):
		# @returns like: [['any', '/path/', 'command']]
		lines = [line.split(":::") for line in config]

		self._verify_values(lines)
		return lines