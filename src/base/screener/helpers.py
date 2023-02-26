import yahooquery as yq
from .models import *
import pandas as pd
from django.conf import settings
import datetime as dt

ARCHIVE_PATH = str(settings.BASE_DIR) + "/archive/"

def downloader(ticker, info, balancesheet, income_statement, cash_flow, history):
    try:
        ticker_object = yq.Ticker(ticker)
        informations = {}
        if info:
            informations['ticker'] = ticker
            informations['name'] = ticker_object.quote_type[ticker]['longName']
            profile = ticker_object.asset_profile[ticker]

            informations['sector'] = profile.get('sector')
            informations['industry'] = profile.get('industry')
            informations['phone'] = profile.get('phone')
            informations['website'] = profile.get('website')
            informations['country'] = profile.get('country')
            informations['state'] = profile.get('state')
            informations['city'] = profile.get('city')
            informations['address'] = profile.get('address1')
            informations['summary'] = profile.get('longBusinessSummary')
            informations['employees'] = profile.get('fullTimeEmployees')
        
        if balancesheet:
            ticker_object.balance_sheet().T.to_csv(ARCHIVE_PATH + 'balancesheet/' + ticker + '.csv')
            informations['balancesheet'] = ticker + '.csv'
        
        if income_statement:
            ticker_object.income_statement().T.to_csv(ARCHIVE_PATH + 'income_statement/' + ticker + '.csv')
            informations['income_statement'] = ticker + '.csv'
        
        if cash_flow:
            ticker_object.cash_flow().T.to_csv(ARCHIVE_PATH + 'cash_flow/' + ticker + '.csv')
            informations['cash_flow'] = ticker + '.csv'

        if history:
            ticker_object.history(period='max').to_csv(ARCHIVE_PATH + 'history/' + ticker + '.csv')
            informations['history'] = ticker + '.csv'


    except Exception as e:
            
        print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
        raise e

    else:

        return informations


def create_object(ticker):

    try:
        informations = downloader(ticker, True, True, True, True, True)


        Company.objects.create(
            ticker = informations['ticker'],
            name = informations['name'],
            
            sector = informations['sector'],
            industry = informations['industry'],
            
            phone = informations['phone'],
            website = informations['website'],
            country = informations['country'],
            state = informations['state'],
            city = informations['city'],
            address = informations['address'],
            
            summary = informations['summary'],
            employees = informations['employees'],

            balancesheet = informations['balancesheet'],
            income_statement = informations['income_statement'],
            cash_flow = informations['cash_flow'],
            history = informations['history'],
        )
        
    except Exception as e:
            
        print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
        raise e

def update_object(ticker):
    try:
        company = Company.objects.filter(ticker=ticker)[0]

        # update the csv files again 
        downloader(ticker, False, True, True, True, False)
        

        history = pd.read_csv(ARCHIVE_PATH + "history/" + str(company.history), index_col = 'date', parse_dates=True)
        latest_date_in_history = history.index.max().to_pydatetime()
        today_date = dt.datetime.today()
        # check if history is updated as current date
        # if the last date in history file is before the current day and is not the weekend
        #       convert to date() all numbers
        if latest_date_in_history.date() < today_date.date() and not (today_date.weekday()== 6 or today_date.weekday() == 5) :
            print("upgrading history")
            # in ticker_info there is the latest updated history csv
            new_df = yq.Ticker(ticker).history(start = latest_date_in_history, end=today_date)
            # concatenate the df
            new_df = pd.concat([history, new_df])
            # eliminate duplicated rows
            new_df = new_df[~new_df.index.duplicated()]
            # save new_df 
            new_df.to_csv(ARCHIVE_PATH + 'history/' + ticker + '.csv')
        else:
            print("already upgraded history")
    
    except Exception as e:
            
        print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
        raise e

    else:
        print("updated object")