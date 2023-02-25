import yahooquery as yq
from .models import *
import pandas as pd
from django.conf import settings

ARCHIVE_PATH = str(settings.BASE_DIR) + "/archive/"

def downloader(ticker, info, balancesheet, income_statement, cash_flow, history):
    try:
        ticker_object = yq.Ticker(ticker)
        informations = {}
        if info:
            informations['ticker'] = ticker
            informations['name'] = ticker_object.quote_type[ticker]['longName']
            profile = ticker_object.asset_profile[ticker]
            informations['sector'] = profile['sector']
            informations['industry'] = profile['industry']
            informations['phone'] = profile['phone']
            informations['website'] = profile['website']
            informations['country'] = profile['country']
            informations['state'] = profile['state']
            informations['city'] = profile['city']
            informations['address'] = profile['address1']
            informations['summary'] = profile['longBusinessSummary']
            informations['employees'] = profile['fullTimeEmployees']
        
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

        