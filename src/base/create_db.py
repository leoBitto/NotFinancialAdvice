import time
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")
django.setup()


import pandas as pd
from screener.helpers import db_manager as manager


tickers_list = pd.read_csv("/home/leonardo/progetti/Finance/src/stocks/big_stock_sectors.csv")


for ticker in tickers_list["Ticker"][:50]:
    time.sleep(5)
    manager.create_object(ticker=ticker)