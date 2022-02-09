# Dividend Analyzer

This application collects current dividend data for a set of stock tickers and analyzes changes in rates and yields. Any such changes are saved in tabular data and reported via email to the user. The intention here is to help investors of dividend paying stocks keep track of changes to dividend payments over time, thus allowing the investor to respond to adverse events like dividend cuts or discontinuations.

---------------

## How Data is Gathered

Data for tickers are pulled from API market data services. The following services are currently supported:
- AlphaVantage
- Polygon\.io
- Yahoo Finance

Some of these services don't have complete data on tickers (eg. AlphaVantage doesn't have dividend payment history) or may be missing data for a ticker entirely. Polygon\.io is currently being used to fetch dividend payment history as it appears to be the most complete and accurate. Other service options may be added in the future, but for now, this app focuses on more free tiered services.

## Usage
**NOTE: This app requires python v3.10 or later**
1. Setup a **config.ini** file (see config section below). Place it in the folder **dividend_analyzer/config**. This file contains configuration variables for the app including API keys and stock ticker list.
2. From app root directory: python setup.py install
3. Verify install: `dividend-analyzer -v`

```
>>> dividend-analyzer
Run a scan of the ticker data and report the results:

>>> dividend-analyzer list-configs
Check the current configs in the config/config.ini file

>>> dividend-analyzer update-configs <your new config.ini file>
Updates the config.ini

```
When run, the app stores data for each ticker in **.csv** files in the **DATA_DIR** folder for each ticker. The data in these files are analyzed for changes in both dividend rate and yield. If there are changes, a report will be generated an then emailed to the recipient configured under **RECEIVER** in the **config.ini** file. The report will show the deltas of the dividend rate and yields of the tickers that changed based on the reference data received.

## Config
Structure your **config.ini** file like below and store in the **config** folder.
```
# API Keys. Only AplhaVantage and Polygon.io need API keys. 
# You can get free keys from them: www.alphavantage.co, www.polygon.io. 
# BOTH keys are need if choosing AlphaVantage as the data source.
[API_KEYS]
ALPHAVANTAGE_API_KEY=your_alphavantage_api_key
POLYGON_API_KEY=your_polygon.io_api_key

# Data Source and Directory. 
# Current options for source are **yahoo** or **alphavantage**, but alphavantange works best so far.
[DATA]
DATA_SOURCE=alphavantage
DATA_DIR=data

# Email Variables. Specify sender and receiver email address along with the email client password. 
# Best to use a separate email account just for this purpose.
[EMAIL_VARS]
SENDER=sender.address@email.com
RECEIVER=receiver.address@email.com
PASS=email_password

# List of Stock Tickers (string of space-separated tickers):
[TICKERS]
TICKER_LIST=AAPL MSFT GOOGL
```
