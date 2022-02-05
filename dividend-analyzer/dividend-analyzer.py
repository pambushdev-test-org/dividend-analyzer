import argparse
import dividend_data
import dividend_analysis
import dividend_alerts
from decouple import config

TICKER_LIST = config('TICKER_LIST')
DATA_SOURCE = config('DATA_SOURCE')
description = 'Runs the app and gathers dividend data. Generates a report after if changes are found.'
version = '0.0.1'

# Command line args parsing for help and version
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-v', '--version', 
	help='Print version number', action='version', 
	version=f'dividend-analyzer v{version}')
args = parser.parse_args()

d = dividend_data.DividendData(TICKER_LIST)
d.check_dividends(DATA_SOURCE)