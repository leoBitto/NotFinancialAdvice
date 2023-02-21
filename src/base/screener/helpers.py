import yahooquery as yq
from models import *

def downloader(ticker, info, balancesheet, income_statement, cash_flow):

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
        informations['balancesheet'] = ticker_object.balance_sheet()
    
    if income_statement:
        informations['income_statement'] = ticker_object.income_statement()
    
    if cash_flow:
        informations['cash_flow'] = ticker_object.cash_flow()
    
    return informations


def create_object(ticker):
    informations = downloader(ticker, True, True, True, True)
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
    )