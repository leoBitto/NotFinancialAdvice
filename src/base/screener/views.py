from django.shortcuts import render
from datetime import datetime as dt
from screener.models import *
from .helpers import *
from .plotter import *
from .index_calculator import *

# Create your views here.
def index(request):
    print(request)
    context={

    }
    return render(request, 'screener/landing.html', context)


def company(request):
    try:
        ticker = request.GET['search_query'].upper()
        #start_date = dt.strptime(request.GET['start_date'], '%Y-%m-%d').replace(tzinfo=timezone.utc)
        #end_date = dt.strptime(request.GET['end_date'], '%Y-%m-%d').replace(tzinfo=timezone.utc)

        company = Company.objects.filter(ticker = ticker)

        if company:
            #update company objects if object is present in db
            update_object(ticker)
            
        else:
            #create company objects
            create_object(ticker)

    ## HANDLE ERRORS
    except Exception as e:
        context = { 
            'req': request.GET['search_query'],
            'error': f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}",
        }
        return render(request, 'screener/404.html', context)

        
    # query db and create context
    company = Company.objects.filter(ticker = ticker)[0]

    # CALCULATE INDICES
    # get income_statement and balancesheet
    income_statement = pd.read_csv(ARCHIVE_PATH + "income_statement/" + str(company.income_statement), index_col=0)
    balancesheet = pd.read_csv(ARCHIVE_PATH + "balancesheet/" + str(company.balancesheet), index_col=0)
    
    indices = calculate_indices(financials = income_statement, balancesheet = balancesheet)
    mean_indices = industry_mean(company.industry)

    # CREATE PLOTS
    # get history



    context={

        'ticker':company.ticker,
        'name':company.name,
        'sector':company.sector,
        'industry':company.industry,
        'phone':company.phone,
        'website':company.website,
        'country':company.country,
        'state':company.state,
        'city':company.city,
        'address':company.address,
        'summary':company.summary,
        'employees':company.employees,

        'balancesheet':company.balancesheet,
        'income_statement':company.income_statement,
        'cash_flow':company.cash_flow,

        'history':company.history,

        'indices':indices,
        'mean_indices':mean_indices,
        
    }

        
    return render(request, 'screener/company.html', context)