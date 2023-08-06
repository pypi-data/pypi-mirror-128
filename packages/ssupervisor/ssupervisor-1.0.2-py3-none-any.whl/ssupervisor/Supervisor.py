import click

from .lib.main import Supervisor
from .lib.config import Config

# To keep things simple, each option here simply
# modifies a particular configuration value
# which the Supervisor class accepts as an 
# argument.
settings = {}

config = Config()

conf_options = {
	'create': config.create,
	'reset': config.reset,
	'edit': config.edit,
	'delete': config.delete,
	'echo': config.echo
}

def set_config(name, value):
	settings.update({ name: value })

def modify_and_inform(name, value, msg):
	set_config(name, value)
	
	if value:
		click.echo(msg)

##########

@click.command()
@click.option('-c', '--conf', default=None)
@click.option('-r', '--recursive', is_flag=True, default=False)
@click.option('-l', '--log', is_flag=True, default=False)
@click.option('-p', '--pass-argument', is_flag=True, default=False)
def cli(conf, recursive, log, pass_argument):
	modify_and_inform('log', log, 'Logging enabled.')
	modify_and_inform('recursive', recursive, 'Recursive walking enabled.')
	modify_and_inform('pass_argument', pass_argument, 'Passing changed file as an argument.')

	if conf:
		try:
			conf_options[conf]()
		except KeyError:
			print(f'"{conf}" is not a configuration command.')
		quit()
	else:
		supervisor = Supervisor(settings)
		supervisor()

##########

if __name__ == '__main__':
	print("MAIN")
	cli()