from django.db import models

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

    balancesheet = models.FileField()
    income_statement = models.FileField()
    cash_flow = models.FileField()
    

    class Meta:
        verbose_name_plural="Companies"
        

    def __str__(self):
        return self.name
