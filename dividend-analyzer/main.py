import dividend_data
import dividend_analysis
import dividend_alerts
from decouple import config

TICKER_LIST = config('TICKER_LIST')
DATA_SOURCE = config('DATA_SOURCE')

d = dividend_data.DividendData(TICKER_LIST)
d.check_dividends(DATA_SOURCE)