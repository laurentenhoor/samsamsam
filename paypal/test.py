import django
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
import sys
import paypalrestsdk
from paypalrestsdk.openid_connect import Tokeninfo, Userinfo
import subprocess
from paypal_helper import Paypal

from django.core import serializers
import urllib,urllib2
import requests
import json

from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives


bills = Bill.objects.filter(user__email=request.session['email'])
bill = bill[0]

for transaction in bill.transaction_set.all():
    print(transaction.user.email) 
    
    
    
from paypal.models import User, Bill, Transaction, Contact

bill = Bill.objects.all()[1]
sender = bill.transaction_set.all()[0]
receiver = bill.transaction_set.all()[1]

contact = Contact(user=sender.user, contact=receiver.user)


contact = Contact(user=sender.user, contact=sender.user)