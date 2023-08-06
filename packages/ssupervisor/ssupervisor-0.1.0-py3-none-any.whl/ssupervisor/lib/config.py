import os
from subprocess import call
from platform import system
from pathlib import Path

from .process import Process

class Config:
	def __init__(self):
		self.config_file = os.path.join(Path.home(), '.supervisor')
		self.process = Process()

	## Creation and Deletion
	def _create_config_file(self):
		try:
			with open(self.config_file, 'x') as supervisor_conf:
				supervisor_conf.write('# Read the Supervisor README')
				
			print(f'Created: {self.config_file}. Use "supervisor -c edit" to modify it.')
		except FileExistsError: # you tell me
			pass

	def _check_config(self):
		if os.path.exists(self.config_file):
			print('You already have a ".supervisor" file in your home folder.')
			quit()
		
		self._create_config_file()

	def _reset_configuration_file(self):
		os.remove(self.config_file)
		
		if input("Create a new configuration file? (y/n) ") == "y":
			self.create()
		else:
			quit()

	def _confirm_reset(self):
		if input('Are you sure? This will delete .supervisor (y/n) ') == 'y':
			self._reset_configuration_file()
		else:
			quit()


	## Handlers
	def _get_config(self):
		try:
			with open(self.config_file, 'r') as conf_file:
				raw_lines = conf_file.readlines()
				lines = [line.strip() for line in raw_lines]

				# Returns all lines that aren't empty and don't
				# start with "#"
				return [line for line in lines if line != "" and line[0] != "#"]
		except FileNotFoundError:
			print('Configuration missing. Please run "supervisor -c create"')
			quit()
	
	def _not_found(self):
		print('.supervisor was not found in your home folder.')

		if input("Create it? (y/n) ") == "y":
			self.create()

	
	def create(self):
		self._check_config()
		self._create_config_file()

	def reset(self):
		if os.path.exists(self.config_file):
			self._confirm_reset()
		else:
			self._not_found()
	
	def edit(self):
		if os.path.exists(self.config_file):
			opener = input('Editor (press Enter for "vim"): ')

			if opener.strip() == "":
				opener = "vim"

			call([opener, self.config_file])
		else:
			self._not_found()

	def delete(self):
		try:
			self._confirm_reset()
		except FileNotFoundError:
			self._not_found()

	def echo(self):
		if os.path.exists(self.config_file):
			with open(self.config_file, 'r') as conf_file:
				print(conf_file.read())
		else:
			self._not_found()