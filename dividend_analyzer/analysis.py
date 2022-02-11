import os
import pandas as pd
import time
import logging
import traceback
import math
from os import listdir
from os.path import isfile, join
from . import alerts
from . import PARENT_DIR, DATA_DIR

class DataAnalysis:
	def __init__(self):
		self.report_data = pd.DataFrame()
		self.has_changed = False

	def process_data(self):
		try:
			if not os.path.exists(os.path.join(PARENT_DIR, DATA_DIR)):
				print('No dividend data found to analyze in the data folder.', flush=True)
			else:
				path = os.path.join(PARENT_DIR, DATA_DIR)
				file_list = [os.path.join(path, f) for f in listdir(path) if isfile(join(path, f))]
				for f in file_list:
					self.analyze_data(file=f)

				if self.has_changed:
					# Generate the report in a csv file and return it
					print('Changes found. Sending report of changes to dividend data...', flush=True)
					if not os.path.exists(os.path.join(PARENT_DIR, 'reports')):
						os.mkdir(os.path.join(PARENT_DIR, 'reports'))
					report_path = os.path.join(PARENT_DIR, 'reports/report.csv')
					self.report_data.to_csv(report_path)
					print(f'Report generated and is located at {report_path}.')					
					return self.report_data
				else:
					print('No changes to report.', flush=True)
					return pd.DataFrame()
		except Exception as err:
			print('Could not process the data.', flush=True)
			traceback.print_exc()

	# Analyze dividend data for tickers based on data from alphavantage
	def analyze_data(self, file):
		data = pd.read_csv(file, index_col=0)
		if data.shape[0] > 1:
			print(f'Checking data in report: {file}', flush=True)
			r_label = 'DividendPerShare'
			y_label = 'DividendYield'
			symbol_label = 'Symbol'
			report_time = time.strftime("%Y-%m-%d %H:%M:%S %p", time.localtime())
			
			symbol = data.iloc[0][symbol_label]
			r1 = data.iloc[0][r_label]
			r2 = data.iloc[1][r_label]
			y1 = data.iloc[0][y_label]
			y2 = data.iloc[1][y_label]
			self.gen_report(r1, r2, y1, y2, r_label, y_label, symbol, report_time)
		else:
			print(f'Not enough data to compare in file {file}', flush=True)

	# Get delta by subtracting the most current value with the previous one. Round to 6 decimal places.
	def calc_delta(self, v1, v2):
		return round(v1 - v2, 6)

	# Generate delta reports for each ticker
	def gen_report(self, r1, r2, y1, y2, r_label, y_label, symbol, report_time):		
		r_delta = self.calc_delta(r1, r2)
		y_delta = self.calc_delta(y1, y2)
		# Checking if these float delta values are close to zero
		r_is_zero = math.isclose(r_delta, 0, rel_tol=1e-6, abs_tol=0)
		y_is_zero = math.isclose(y_delta, 0, rel_tol=1e-6, abs_tol=0)

		if not r_is_zero or not y_is_zero:
			if not self.has_changed: 
				self.has_changed = True
			df = pd.DataFrame(
				{
					'Symbol': symbol,
					f'Current{r_label}'	: r1,
					f'Prev{r_label}'	: r2, 
					f'{r_label}Delta'	: r_delta,
					f'Current{y_label}'	: y1, 
					f'Prev{y_label}'	: y2, 
					f'{y_label}Delta'	: y_delta					
				}, index=[report_time]
			)
			self.report_data = pd.concat([df, self.report_data])			
		else:
			print(f'No diffs for {symbol}, nothing to report.', flush=True)	