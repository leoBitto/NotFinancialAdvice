import time
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")
django.setup()


import pandas as pd
from screener.helpers import db_manager as manager


tickers_list = pd.read_csv("/home/leonardo/progetti/NFA/ItalianTickerList.csv")
counter = 200
unread_tickers = []
for ticker in tickers_list["Ticker symbol"][200:300]:
    print("Trying to download ticker with symbol: ", ticker)
    time.sleep(2)
    try:
        manager.create_object(ticker=ticker)
        counter += 1
        print("downloaded ", ticker, " number ", counter)
    except Exception as e:
        unread_tickers.append(ticker)
        print(e)
    finally:
        continue

print(unread_tickers)

