import sys
import argparse
from conf import config
import data
from version import version

description = 'Runs the app and gathers dividend data. Generates a report if changes are found.'
CONFIG_DIR = 'conf'

def call_display_configs():
	config.display_configs(CONFIG_DIR)
	sys.exit()

def call_update_configs(file):
	config.update_configs(file, CONFIG_DIR)
	sys.exit()

FUNCTION_MAP = {
	'list-configs' : call_display_configs,
	'update-configs' : call_update_configs
}

def main(args=None):
	if args is None:
		args = sys.argv[1:]

	# Command line args parsing for help and version
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('-v', '--version', 
		help='Print version number', action='version', 
		version=f'dividend-analyzer v{version}'
	)
	parser.add_argument('command', nargs='?',
		help='Display or update configs in the config.ini file',
		choices=FUNCTION_MAP.keys()
	)
	parser.add_argument('config_file', nargs='?')
	
	args = parser.parse_args()
	
	# Execute cli commands for configs if present
	if args.command:
		config_func = FUNCTION_MAP[args.command]
		if config_func == call_update_configs:
			if args.config_file:
				config_func(args.config_file)
			else:
				print('No config file provided to update configs.')
				sys.exit()
		else:
			config_func()

	# Get configs and run the dividend checker
	configs = config.get_configs(CONFIG_DIR)
	TICKER_LIST = configs['TICKERS']['TICKER_LIST']
	DATA_SOURCE = configs['DATA']['DATA_SOURCE']	
	d = data.DividendData(TICKER_LIST)
	d.check_dividends(DATA_SOURCE)

if __name__ == "__main__":
    sys.exit(main())