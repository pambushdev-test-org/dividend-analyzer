from configparser import ConfigParser
from os import path

curr_dir = path.abspath(path.dirname(__file__))
CONFIG_DIR = path.join(curr_dir, 'config')

# Get configs from config.ini file
def get_configs():	
	config_object = ConfigParser()
	if path.exists(path.join(CONFIG_DIR, 'config.ini')):
		# Get configs from config.ini
		config_object.read(path.join(CONFIG_DIR, 'config.ini'))
		return config_object
	else:
		print(f'Config file in location "{CONFIG_DIR}" does not exist', flush=True)
		print(f'Current directory: {curr_dir}')

# Print configs from config.ini file
def display_configs():
	config_object = ConfigParser()
	if path.exists(path.join(CONFIG_DIR, 'config.ini')):
		# Get configs from config.ini
		config_object.read(path.join(CONFIG_DIR, 'config.ini'))
		for section in config_object.sections():
			print({section: dict(config_object[section])})
	else:
		print(f'Config file in location "{CONFIG_DIR}" does not exist', flush=True)

# Update the configs in the config.ini file. Will replace everything inside with what's in {file}.
def update_configs(file):
	config_object = ConfigParser()
	if path.exists(file):
		conf = open(file)
		with open(path.join(CONFIG_DIR, 'config.ini'), 'w') as f:
			f.writelines(conf)
		print('Configs in config.ini have been updated.', flush=True)
	else:
		print(f'Config update failed. File does not exist: {file}', flush=True)