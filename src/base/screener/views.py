from django.shortcuts import render
from datetime import datetime as dt
from datetime import timezone
from screener.models import *
from .helpers import *

# Create your views here.
def index(request):
    print(request)
    context={

    }
    return render(request, 'screener/landing.html', context)


def company(request):
    
    ticker = request.GET['search_query'].upper()
    start_date = dt.strptime(request.GET['start_date'], '%Y-%m-%d').replace(tzinfo=timezone.utc)
    end_date = dt.strptime(request.GET['end_date'], '%Y-%m-%d').replace(tzinfo=timezone.utc)

    company = Company.objects.filter(ticker = ticker)

    if company:
        #update company objects
        pass
    else:
        #create company objects
        create_object(ticker, )

    context={

    }
    return render(request, 'screener/company.html', context)