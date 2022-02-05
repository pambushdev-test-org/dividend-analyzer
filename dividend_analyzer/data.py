import yfinance as yf
import json
import time
import requests
import pandas as pd
import os
import logging
import traceback
from decouple import config
from . import analysis

DATA_DIR = 'data'
logging.basicConfig(filename='logs/logs.txt', encoding='utf-8', 
					format='%(asctime)s %(message)s', datefmt='%Y/%m/%d/ %I:%M:%S %p', 
					level=logging.DEBUG)

class DividendData():
	
	def __init__(self, tickers):
		self.tickers = tickers
		self.ticker_objs = {}
		self.ticker_data = {}
		self.scraped_data = {}

	# Checks a list of stock tickers if they are currently paying dividends. Input is ticker data from yfinance.
	def check_dividends(self, source):		
		print('Checking status of dividends...', flush=True)
		try:
			self.get_ticker_data(source=source)
			self.scrape_dividend_data(source=source)			
			self.gen_report()
			# Go process all the data received
			d = analysis.DataAnalysis()
			d.process_data()
		except Exception as err:
			print(f'Could not get ticker data from {source}.', flush=True)
			traceback.print_exc()

	# Get ticker data using Yahoo finance API
	def get_ticker_data(self, source):
		match source:
			case 'yahoo':
				try:
					self.ticker_objs = yf.Tickers(self.tickers).tickers
					# Ticker.info is an expensive operation. Getting the info for all tickers here so that this operation isn't called later.
					print(f'Getting ticker data from yfinance for {len(self.ticker_objs)} tickers...', flush=True)
					self.ticker_data = {}
					count = 0
					for i in self.ticker_objs:
						start_time = time.time()
						self.ticker_data[i] = self.ticker_objs[i].info
						t = time.time() - start_time
						count += 1
						print(f'Data for ticker {i} received in {t}s. Progress: [{count}/{len(self.ticker_objs)}]')
				except:
					print("Could not get ticker data from Yahoo Finance. List of tickers may not have been provided.", flush=True)
			case 'alphavantage':
				API_KEY = config('ALPHAVANTAGE_API_KEY')
				try:
					# Input is a string of space separated tickers. Convert to a list here for iteration later.
					tickers_list = list(self.tickers.split(' '))
					print(f'Getting ticker data from AlphaVantage for {len(tickers_list)} tickers...', flush=True)
					count = 0
					for i in tickers_list:
						start_time = time.time()
						url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={i}&apikey={API_KEY}'
						r = requests.get(url)
						self.ticker_data[i] = r.json()

						# API limit is 5 per minute. Sleep here for 15s.
						time.sleep(15)
						t = time.time() - start_time
						count += 1						
						print(f'Data for ticker {i} received in {t}s. Progress: [{count}/{len(tickers_list)}]', flush=True)
				except Exception as err:
					print('Could not get ticker data from AlphaVantage. List of tickers may not have been provided.', flush=True)
					traceback.print_exc()
			case _:
				print('No API data source specified.', flush=True)

	# Scrape the downloaded ticker data for dividend info. Store results in a table.
	def scrape_dividend_data(self, source):
		match source:
			case 'yahoo':
				# Process Yahoo data
				for s in self.ticker_data:
					# Check if dividend data exists in received data
					if 'dividendRate' and 'trailingAnnualDividendRate' and 'trailingAnnualDividendYield' in self.ticker_data[s]:
						if self.ticker_data[s]['dividendRate'] == 0 and self.ticker_data[s]['trailingAnnualDividendRate'] == 0 and self.ticker_data[s]['trailingAnnualDividendYield'] == 0:
							print(f'***Stock {self.ticker_data[s]["symbol"]} does NOT currently pay a dividend.', flush=True)
						else: 
							print(f'Stock {self.ticker_data[s]["symbol"]} pays a dividend of ${str(self.ticker_data[s]["trailingAnnualDividendRate"], flush=True)} per share annually.')
							# Add info for this ticker to scraped data. Includes dividend rate, trailing rate, yield, and last 4 dividend payments
							self.scraped_data[s] = {
								'dividendRate': self.ticker_data[s]['dividendRate'],
								'trailingAnnualDividendRate': self.ticker_data[s]['trailingAnnualDividendRate'],
								'trailingAnnualDividendYield': self.ticker_data[s]['trailingAnnualDividendYield'],
								'symbol': self.ticker_data[s]['symbol']
							}
					else:
						print(f'No dividend rate and yield data from {source} for {s}. Calculating from dividend payment history...', flush=True)
						self.scraped_data[s] = self.get_dividend_payments(source='polygon', ticker=s)
			case 'alphavantage':
				# Process alphavantage data
				for s in self.ticker_data:
					# Check if dividend rate data and yield exists in received data
					if 'DividendPerShare' and 'DividendYield' in self.ticker_data[s]:
						# Numerical values in alphavantage data are stored as strings. Casting to floats here.						
						self.scraped_data[s] = {
							'DividendPerShare': float(self.ticker_data[s]['DividendPerShare']),
							'DividendYield': float(self.ticker_data[s]['DividendYield']),
							'Symbol': self.ticker_data[s]['Symbol']
						}
					else:						
						print(f'No dividend rate and yield data from {source} for {s}. Calculating from dividend payment history...', flush=True)						
						# Check dividend history and calculate trailing rate and yield. Use polygon.io API for this.
						self.scraped_data[s] = self.get_dividend_payments(source='polygon', ticker=s)
			case _:
				pass

	# Get dividend payments for a ticker.
	def get_dividend_payments(self, source, ticker):
		match source:
			case 'yahoo':
				try:					
					divs = self.ticker_objs[ticker].dividends					
					last12divs = divs[len(divs) - 13: len(divs) - 1]
					return last12divs
				except (AttributeError, ValueError) as err:
					print(f'Could not get dividend payment info for {ticker} from Yahoo.', flush=True)
					return {'data_missing': ''}
			case 'polygon':
				# Process polygon.io dividend payment data
				API_KEY = config('POLYGON_API_KEY')
				limit = 12
				try:
					# Get last 12 dividend payments for ticker
					url = f'https://api.polygon.io/v3/reference/dividends?ticker={ticker}&limit={limit}&apiKey={API_KEY}'
					r = requests.get(url)
					divs = r.json()['results']					
					# API limit is 5 per minute. Sleep here for 15s.
					time.sleep(15)

					# Get last ticker close price, dividend frequency, and dividend payments then calculate dividend rate and yield
					url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?apiKey={API_KEY}'
					r = requests.get(url)
					ticker_close_price = r.json()['results'][0]['c']
					frequency = divs[0]['frequency']
					dividend_payments_total = 0
					time.sleep(15)

					print(f'Dividend Data for ticker {ticker} received.', flush=True)
					
					# Iterate over the divs payments and get {frequency} amount of them
					count = frequency
					for i in divs:
						dividend_payments_total += i['cash_amount']
						count -= 1
						if count == 0:
							break					
					
					data = {
						'DividendPerShare': dividend_payments_total,
						'DividendYield': dividend_payments_total / ticker_close_price,
						'Symbol': ticker # Fill in missing symbol data here						
					}
					return data
				except Exception as err:
					print(f'Could not get dividend payment info for {ticker} from polygon.io.', flush=True)
					data = {
						'DividendPerShare': '',
						'DividendYield': '',
						'Symbol': ticker
					}
					traceback.print_exc()
					return data
			case _:
				pass

	# Generate printed report of dividend status and data. Store in the data folder.
	def gen_report(self):
		if not os.path.exists(DATA_DIR):
			os.mkdir(DATA_DIR)
		data_dir = DATA_DIR
		parent_dir = os.getcwd()
		path = os.path.join(parent_dir, DATA_DIR)
		print('Generating reports...', flush=True)
		for s in self.scraped_data:
			target = os.path.join(path, s)
			report_time = time.strftime("%Y-%m-%d %H:%M:%S %p", time.localtime())
			new_data = pd.DataFrame(self.scraped_data[s], index=[report_time])

			if not os.path.exists(f'{target}.csv'):				
				new_data.to_csv(f'{target}.csv')
			# Read data from existing csv file for ticker, append new data, then write back to file. Store data in reverse chrono order.
			else:
				data = pd.read_csv(f'{target}.csv', index_col=0)
				data = pd.concat([new_data, data])
				data = data.drop_duplicates()

				# Keep only the last 100 entries of data
				num_rows = data.shape[0]
				if num_rows > 100:
					data = data.drop(data.tail(1).index)
				data.to_csv(f'{target}.csv')
		print('Reports completed.', flush=True)