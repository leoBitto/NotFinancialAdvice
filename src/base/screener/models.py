from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage

path_balancesheet = FileSystemStorage('/balancesheet')
path_income_statement = FileSystemStorage('/income_statement')
path_cash_flow = FileSystemStorage('/cash_flow')
path_history = FileSystemStorage('/history')

# Create your models here.
class Company(models.Model):

    ticker = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    
    sector = models.CharField(max_length=100, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    
    phone = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    
    summary = models.TextField(blank=True, null=True)
    employees = models.IntegerField(blank=True, null=True)

    balancesheet = models.FileField(upload_to = path_balancesheet, blank=True, null=True)
    income_statement = models.FileField(upload_to = path_income_statement, blank=True, null=True)
    cash_flow = models.FileField(upload_to = path_cash_flow, blank=True, null=True)
    history = models.FileField(upload_to=path_history, blank=True, null=True)

    class Meta:
        verbose_name_plural="Companies"
        

    def __str__(self):
        return self.name
