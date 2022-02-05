Dividend Analyzer
========================

This application collects current dividend data for a set of stock tickers and analyzes changes in rates and yields. Any such changes are saved in tabular data and reported via email to the user. The intention here is to help investors of dividend paying stocks keep track of changes to dividend payments over time, thus allowing the investor to respond to adverse events like dividend cuts or discontinuations.

---------------

How Data is Gathered
--------------------
Data for tickers are pulled from API market data services. The following services are currently supported:

- AlphaVantage
- Polygon.io
- Yahoo Finance

Some of these services don't have complete data on tickers (eg. AlphaVantage doesn't have dividend payment history) or may be missing data for a ticker entirely. Polygon.io is currently being used to fetch dividend payment history as it appears to be the most complete and accurate. Other service options may be added in the future, but for now, this app focuses on more free tiered services.

Usage
------------------
1. In the app root folder, make a file called **.env**
2. The .env file contains environment variable for the app. See the Environment Variables section below on how to setup.
3. python setup.py
4. python build/lib/dividend-analyzer/main.py

App store data for each ticker in **.csv** files in the **data** folder for each ticker. The data in these files are analyzed for changes in both dividend rate and yield. If there are changes, a report will be generated an then emailed to the configured recipient under RECEIVER in the **.env** file. The report will show the deltas of the dividend rate and yields of the tickers that changed based on the reference data received.

Environment Variables
---------------------
Structure your **.env** file like below.

# API Keys:
^^^^^^^^^^^

ALPHAVANTAGE_API_KEY=your_api_key

POLYGON_API_KEY=your_api_key

# Data Source:
^^^^^^^^^^^^^^
# Current options are yahoo or alphavantage, but alphavantange works best here so far

DATA_SOURCE=alphavantage

# Email:
^^^^^^^^

SENDER=sender.address\@email.com

RECEIVER=receiver.address\@email.com

PASS=email_password

List of Stock Tickers (string of space-separated tickers):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TICKER_LIST='AAPL MSFT GOOGL'