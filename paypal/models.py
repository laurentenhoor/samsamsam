from django.db import models
from django.db.models import Sum
from decimal import Decimal
from datetime import datetime
from django.utils import timezone

class User(models.Model):
    email = models.EmailField(max_length=70, unique=True)
    validated = models.BooleanField()
    free_transactions = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email
    
class Contact(models.Model):
    user = models.ForeignKey(User, related_name='main_user')
    contact = models.ForeignKey(User, related_name='user_contact')
    last_used = models.DateTimeField(default=datetime.now)
    
    class Meta:
        unique_together = ('user', 'contact',)
        ordering = ['-last_used']
        
    def __str__(self):
        return str(self.user.email) + ' - ' + str(self.contact.email)
     


class Bill(models.Model):
    user = models.ForeignKey(User)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)
    paykey = models.CharField(max_length=40, default="", blank=True)
    reminder_date = models.DateTimeField(default=timezone.now)
    
    @property
    def reminder_date_difference(self):
        timediff = timezone.now() - self.reminder_date
        return timediff.total_seconds()
    
    @property
    def sum(self):
        sum = self.transaction_set.filter(status='Paid').aggregate(Sum('amount'))['amount__sum']
        return 0.00 if sum == None else sum
    
    @property
    def percentage(self):
        return Decimal(self.sum/self.amount)*100
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return self.description
    
class Transaction(models.Model):
    bill = models.ForeignKey(Bill)
    user = models.ForeignKey(User)
    amount = models.DecimalField(decimal_places=2, max_digits=100)
    status = models.CharField(max_length=10)
    hash = models.CharField(max_length=10, default="")
    paykey = models.CharField(max_length=40, default="", blank=True)
    paykey_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return Bill.objects.get(id=self.bill.id).description + ' (' +str(self.amount)+')'
    
    