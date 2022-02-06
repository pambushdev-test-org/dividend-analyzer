from configparser import ConfigParser
from os.path import join, exists

# Get configs from config.ini file
def get_configs(CONFIG_DIR):
	config_object = ConfigParser()
	if exists(join(CONFIG_DIR, 'config.ini')):
		# Get configs from config.ini
		config_object.read(join(CONFIG_DIR, 'config.ini'))
		return config_object
	else:
		print(f'Config file does not exist', flush=True)

# Print configs from config.ini file
def display_configs(CONFIG_DIR):
	config_object = ConfigParser()
	if exists(join(CONFIG_DIR, 'config.ini')):
		# Get configs from config.ini
		config_object.read(join(CONFIG_DIR, 'config.ini'))
		for section in config_object.sections():
			print({section: dict(config_object[section])})
	else:
		print(f'Config file does not exist', flush=True)

# Update the configs in the config.ini file. Will replace everything inside with what's in {file}.
def update_configs(file, CONFIG_DIR):
	config_object = ConfigParser()
	if exists(file):
		conf = open(file)
		with open(join(CONFIG_DIR, 'config.ini'), 'w') as f:
			f.writelines(conf)
		print('Configs in config.ini have been updated.', flush=True)
	else:
		print(f'Config update failed. File does not exist: {file}', flush=True)