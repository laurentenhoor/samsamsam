from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
import sys
import paypalrestsdk
from paypalrestsdk.openid_connect import Tokeninfo, Userinfo
import subprocess
from django.utils.crypto import get_random_string

from models import User, Bill, Transaction, Contact
from paypal_helper import Paypal

from django.core import serializers
import urllib,urllib2
import requests
import json

from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from django.utils import timezone

from celery.decorators import task
import tasks
from _sqlite3 import IntegrityError

URL_PREFIX = 'http://www.samsamsam.nl'
UNDER_CONSTRUCTION = False
ADMIN = ['henknozemans@outlook.com', 'info@samsamsam.nl'] #


# REST API
# paypalrestsdk.configure({
#       "mode": "sandbox",
#       "client_id": "AfOXYhDKDLORvA-9AjyHFi3Vc2wybslr0sYBBk7tzw-9wfaoS-UBTdQFEb5c",
#       "client_secret": "EP5JQxAG7TYxAargPTnf31oAonOpfZJ5v5Ud4EqmQwwKxIHvvbMmpfP94wVU",
#       "openid_redirect_uri": "http://www.samsamsam.nl/login_return"
#     })
paypalrestsdk.configure({
      "mode": "live",
      "client_id": "AU4i0hCql7KtqKumQMvaL48EQEqJwQJBjyBcG8MyMoxkKjauHp_SpeJ319cv",
      "client_secret": "EG54cBBvMl66sVcFu2R2ksXfm9NeLVq1a4O7xHv9sSQVk7bxeWo20m5YDqqJ",
      "openid_redirect_uri": "http://www.samsamsam.nl/login_return"
    })


def login_as(request, email):
    if not request.session['email'] == 'laurentenhoor@gmail.com':
        return HttpResponseRedirect(reverse('paypal:logout'))
    
    if User.objects.filter(email = email).count():
        request.session['email'] = email
    
    return HttpResponseRedirect('/')
    


def reminder(request, billPk):
    needs_login = checkLogin(request)
    if needs_login:
        return needs_login
    
    bill = Bill.objects.get(pk=billPk)
    bill.reminder_date = timezone.now()
    bill.save()

    if not bill.user.email == request.session['email']:
        return HttpResponseRedirect(reverse('paypal:logout'))
       
    unpaid_transactions = bill.transaction_set.all().filter(status='Unpaid')
       
    mails=[]
    
    for unpaid_transaction in unpaid_transactions:
        mails.append(createMail(unpaid_transaction.user.email, unpaid_transaction, bill, True))
        
    connection = mail.get_connection()
    connection.open()
    connection.send_messages(mails)
    connection.close()
        
    return HttpResponseRedirect(reverse('paypal:overview'))
    
    
def checkLogin(request):
    
    try:
        email = request.session['email']
        
        if UNDER_CONSTRUCTION and not email in ADMIN:
            return render(request, 'paypal/construction.html', {})
        
    except KeyError:
        return HttpResponseRedirect('/')
    
    return None


def construction(request):
    return render(request, 'paypal/construction.html', {})


def email_template(request):
    return render(request, 'paypal/email_template.html', {})


def new_bill(request):    
    needs_login = checkLogin(request)
    if needs_login:
        return needs_login
    
    myemail = request.session['email']
    
    print('Loading bill editor ('+request.session['email']+')')
    
    emails = Contact.objects.filter(user__email=myemail).values_list('contact__email', flat=True)
    
    return render(request, 'paypal/edit_bill.html', {'transaction_emails' : [] ,'other_emails' : emails, 'me' : myemail, "me_active" : True})


def delete_bill(request, pk):
    
    bill = Bill.objects.get(pk=pk)

    if bill.user.email == request.session['email']:
        bill.delete()
    else:
        return HttpResponseRedirect(reverse('paypal:logout'))

    return HttpResponseRedirect(reverse('paypal:overview'));

def edit_bill(request, pk):
    needs_login = checkLogin(request)
    if needs_login:
        return needs_login
    
    bill = Bill.objects.get(pk=pk)
    if not bill.user.email == request.session['email']:
        return HttpResponseRedirect(reverse('paypal:logout'))
    elif bill.status == "Paid":
        return HttpResponseRedirect(reverse('paypal:overview'))
    
    
    myemail = request.session['email']
    me_active = True
    
    contact_emails = Contact.objects.filter(user__email=myemail).values_list('contact__email', flat=True)
    
    transactions = bill.transaction_set.all()
    transaction_emails = bill.transaction_set.all().values_list('user__email', flat=True)
    
    other_emails = list(set(contact_emails) - set(transaction_emails))
    
    if myemail in transaction_emails:
        transaction_emails = list(set(transaction_emails) - set([myemail]))
        me_active = True
    else:
        me_active = False
    
    print(transactions[0])

  
    return render(request, 'paypal/edit_bill.html', {'transactions' : transactions, 'transaction_emails' : transaction_emails ,'other_emails' : other_emails, 'me' : myemail, "me_active" : me_active, 'bill':  bill})


def overview(request):
    needs_login = checkLogin(request)
    if needs_login:
        return needs_login
    
    print('Loading overview ('+request.session['email']+')')
    
    
    confirmed_bills = Bill.objects.filter(user__email=request.session['email'], status="Paid")
    unconfirmed_bills = Bill.objects.filter(user__email=request.session['email'], status="Created")
     
    # check for unpaid payments
    transactions_to_check = Transaction.objects.filter(bill__user__email=request.session['email'], bill__status="Paid", status="Unpaid").exclude(paykey=u'')
    
    if transactions_to_check:
        print('Found some conflicts in transactions.')
        print(transactions_to_check)
     
    for transaction in transactions_to_check:
        if getStatus(transaction.paykey) == "COMPLETED":
            transaction.status = 'Paid'
        elif (timezone.now() - transaction.paykey_date > timezone.timedelta(minutes=2)):
            transaction.paykey = '' # TODO: mistake if screen is reloaded during a payment
            print('Removed Paykey')
        transaction.save()
    
    return render(request, 'paypal/overview.html', {'confirmed_bills': confirmed_bills, 'unconfirmed_bills': unconfirmed_bills})

def privacy_policy(request):
    return render(request, 'paypal/policies.html', {"content": ""})

def user_agreement(request):
    return render(request, 'paypal/policies.html', {"content": ""})

def validate(request, paykey):
    return render(request, 'paypal/validate.html', {'paykey' : paykey})

def user(request, email):
    
#     if request.method == 'POST':
    user = checkUser(email, False)
    me = User.objects.filter(email=request.session['email'])[0]
    
    if user.email == me.email:
        return HttpResponse()
#         return HttpResponse(json.dumps({"id": 'this is me!'}), content_type="application/json")
    
    contact = Contact(user=me, contact=user)
    contact.save()

    return HttpResponse(json.dumps({"id": user.pk}), content_type="application/json")

def user_delete(request, email):
        
    contact = Contact.objects.filter(user__email=request.session['email'],contact__email=email)[0]
    contact.delete()
    
    return HttpResponse(json.dumps({"status": 'success'}), content_type="application/json")


def createMail(email, transaction, bill, isReminder):
    
    subjectPrefix = 'Herinnering! ' if isReminder else ''
    subject, from_email, to = subjectPrefix+bill.description + ' (' + u"\u20AC" + ' '+ str(transaction.amount) + ')', 'Samsamsam <info@samsamsam.nl>', email
    text_content = 'Login op www.samsamsam.nl om jouw rekening te betalen.'
    
    htmly = get_template('paypal/email_template.html')
    d = Context({'bill': bill, 'transactions': bill.transaction_set.all(),  'user': bill.user, 'description' : bill.description, 'amount' : transaction.amount, 'transaction_hash' : transaction.hash, 'url_prefix' : URL_PREFIX})
    
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    return msg


def save_bill(request, pk=False):
    needs_login = checkLogin(request)
    if needs_login:
        return needs_login
    
    totalAmount = float(request.POST.get('amount'))
     
    user = checkUser(request.session['email'])
    
    if pk:
        bill = user.bill_set.get(pk=pk)
        if bill.status == 'Paid':
            return 'deze is niet te wijzigen'
        bill.delete()
    
    bill = user.bill_set.create(
                                amount=totalAmount,
                                description=request.POST.get('description'),
                                user=user,
                                status="Created"
                                )
    bill.save()
    request.session['bill_id'] = bill.id
     
    transaction_emails = request.POST.getlist('email_list')
    transaction_amounts = request.POST.getlist('amount_list')
    
    splittedAmount = totalAmount / len(transaction_emails)
     
    for idx, email in enumerate(transaction_emails):
        
        transaction_user = checkUser(email)
        
        if not request.session['email'] == email:
            contact = Contact.objects.get(user__email=request.session['email'], contact__email=email)
            contact.last_used = timezone.now()
            contact.save()
        
        
        
        
        bill.transaction_set.create(
                                    user=transaction_user,
                                    amount=transaction_amounts[idx],
                                    status='Unpaid' if not email == request.session['email'] else 'Paid',
                                    )
    bill.save()

#     return render(request, 'paypal/create_bill.html', {'bill': bill})
    return HttpResponseRedirect(reverse('paypal:overview'))
    
    
    
def refreshToken(request):
    
    refreshtoken = request.session['refresh_token']
    tokeninfo = Tokeninfo.create_with_refresh_token(refreshtoken)
    request.session['id_token'] = tokeninfo.id_token
    request.session['access_token'] = tokeninfo.access_token
    
    

def seamless(request, pk):
    needs_login = checkLogin(request)
    if needs_login:
        return needs_login
    
#     Todo: optimalization of speed? This step takes long!
#     if 'refresh_token' in request.session:
#         refreshToken(request)

    if User.objects.get(email=request.session["email"]).free_transactions == True:
        
        bill = Bill.objects.get(pk=pk, user__email=request.session["email"])
        
        if not bill.status == 'Paid':
            bill.status = 'Paid'
            bill.save()
            createTransactions(request, bill)
        
        return HttpResponseRedirect(reverse('paypal:overview'))
    
    request.session['bill_id'] = pk
    
    paypal = Paypal()
    
    if 'access_token' in request.session:
        access_token = request.session['access_token']
    else:
        access_token = ''
                                           
    express_token = paypal.SetExpressCheckout(access_token)
    url = paypal.PAYPAL_URL + express_token
    
    print('Express token: '+express_token)
    
    return HttpResponseRedirect(url)
    
    
    
def mass_pay(request):
    
    paypal = Paypal()
    tokens = paypal.MassPay('laurentenhoor@gmail.com', 1.00, 'Eerste betaling', 'Eerste betaling')
    
    return HttpResponse(json.dumps(tokens), content_type="application/json")


    
def test_personal_express(request):
            
    paypal = Paypal()        
    
    if 'access_token' in request.session:
        access_token = request.session['access_token']
    else:
        access_token = ''
                                           
    express_token = paypal.SetExpressCheckout(access_token)
    url = paypal.PAYPAL_URL + express_token
    
    print('Express token: '+express_token)
    
    return HttpResponseRedirect(url)



        
def checkUser(email, validated=False):
    
    user = User.objects.filter(email=email)
    
    if user.exists():
        user = user[0]
        if validated == True:
            user.validated = True
            user.save()
    else:
        user = User(email=email, validated=validated, free_transactions=True)
        user.save()
    
    return user


def afterLogin(request):
    
    print('Logged in ('+request.session['email']+')')
   
    if Bill.objects.all().filter(user__email=request.session['email']).count():
        return HttpResponseRedirect(reverse('paypal:overview'))
    return HttpResponseRedirect(reverse('paypal:input_bill'))
    

def login(request):
    
    print('Starting point')
    
    if 'logout_url' not in request.session:
        # Generate login url
        login_url = Tokeninfo.authorize_url({ "scope": "openid profile email"}) #{ "scope": "openid profile email https://uri.paypal.com/services/expresscheckout"}
        return HttpResponseRedirect(login_url)
    
    else:
        return afterLogin(request)


def payment_do(request):
    needs_login = checkLogin(request)
    if needs_login:
        return needs_login
     
    paypal = Paypal()
    
    #     express_token = paypal.GetExpressCheckoutDetails(pp_token) #?get token if not seamless?
    token = request.GET['token']
    payer_id = request.GET['PayerID']
    
    response_tokens = paypal.DoExpressCheckoutPayment(token, payer_id)
    
    transaction_id = response_tokens['PAYMENTINFO_0_TRANSACTIONID']
    status = response_tokens['PAYMENTINFO_0_PAYMENTSTATUS']
#     message = response_tokens['L_SHORTMESSAGE0']
        
    bill = Bill.objects.get(pk=request.session['bill_id'])
    
    if bill.status == 'Paid':
        HttpResponseRedirect(reverse('paypal:overview'))      
    bill.status = 'Paid' if status == 'Completed' else 'Unpaid'
    bill.paykey = transaction_id
    bill.save()
    
    if bill.status == 'Paid':
         createTransactions(request, bill)
    
#     print('Message: '+ message)
    
#     details = paypal.GetTransactionDetails(transaction_id)
#     print(details)

#     return render(request, 'paypal/payment_return.html', {'status': status})
    return HttpResponseRedirect(reverse('paypal:overview'))

def test(request):
    
    subject, from_email, to = 'Nieuwe Samsamsam 2', 'Samsamsam <info@samsamsam.nl>', ['lauren.ten.hoor@philips.com', 'laurentenhoor@gmail.com', 'henknozemans@outlook.com']
    text_content = 'Login op beta.samsamsam.nl om jouw rekening te betalen.'
    
    htmly = get_template('paypal/email_template_beta2.html')
    d = Context({})
    
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    
    connection = mail.get_connection()
    # Manually open the connection
    connection.open()
    # Send the two emails in a single call -
    connection.send_messages([msg])
    # The connection was already open so send_messages() doesn't close it.
    # We need to manually close the connection.
    connection.close()
    
    return render(request, 'paypal/email_template_beta2.html', {})  
    
    
    
def createTransactions(request, bill):
    
    print('createTransactions')
    mails = []
    
    for transaction in bill.transaction_set.all():
        sender = transaction.user
        
        for transaction2 in bill.transaction_set.all():
            receiver = transaction2.user
            if not sender == receiver:
                if not Contact.objects.filter(user=receiver, contact=sender).count():
                    contact = Contact(user=receiver, contact=sender)
                    contact.save()             
        
        amount = transaction.amount
        description = bill.description
        receiver = bill.user.email
        transaction.hash = get_random_string(length=10)
        transaction.save()
        if not sender.email == request.session['email']:
            mails.append(createMail(sender.email, transaction, bill, False))
        
    
    
    mails.append(createMail('laurentenhoor@gmail.com', transaction, bill, False))
    
#     print('Before Sending Emails')
    bill.save()
    
#     sendEmails.delay(mails)
    connection = mail.get_connection()
    # Manually open the connection
    connection.open()
    # Send the two emails in a single call -
    connection.send_messages(mails)
    # The connection was already open so send_messages() doesn't close it.
    # We need to manually close the connection.
    connection.close()
    



def return_email(request, transaction_hash):
    
    transactions = Transaction.objects.filter(hash=transaction_hash)

    if not transactions:
        return HttpResponseRedirect(reverse('paypal:overview'))
    
    transaction = transactions[0]
    
    bill = transaction.bill

    request.session['email'] = transaction.user.email
    
    if transaction.status == 'Paid':
        return HttpResponseRedirect(reverse('paypal:overview'))
    
    if not transaction.paykey:
        paykey = createPersonalPaymentKey(bill.user.email, transaction.amount, bill.description, transaction_hash)
        transaction.paykey = paykey
        transaction.paykey_date = timezone.now()
        transaction.save()
    else: 
        paykey = transaction.paykey
    
    cgi = 'https://www.paypal.com/cgi-bin/webscr?cmd=_ap-payment&paykey='
#     webapps = 'https://www.paypal.com/webapps/adaptivepayment/flow/pay?paykey='    
    return HttpResponseRedirect(cgi+paykey)
          
          

def return_personal_payment(request, transaction_hash):
    
    transaction = Transaction.objects.get(hash=transaction_hash)
    
    status = getStatus(transaction.paykey)
    print(status)
    
    if status == 'COMPLETED':
        transaction.status = 'Paid'
        transaction.save()
    
    return HttpResponseRedirect('/')


        
def createPersonalPaymentKey(receiver, amount, description, transaction_hash):
    
    paypal_api = "Pay";
    
    # Adaptive payments
#     PAYPAL_PREFIX = "https://svcs.sandbox.paypal.com/AdaptivePayments/" #SANDBOX
#     PAYPAL_HEADERS = { # SANDBOX
#            "X-PAYPAL-SECURITY-USERID" : "laurentenhoor-facilitator_api1.gmail.com",
#            "X-PAYPAL-SECURITY-PASSWORD" : "1403877035",
#            "X-PAYPAL-SECURITY-SIGNATURE" : "AFcWxV21C7fd0v3bYYYRCpSSRl31AnxMpEgWsQEZ1e7xxrMOYanv5NV8",
#            "X-PAYPAL-APPLICATION-ID" : "APP-80W284485P519543T",
#            "X-PAYPAL-REQUEST-DATA-FORMAT" : "JSON",
#            "X-PAYPAL-RESPONSE-DATA-FORMAT" : "JSON",
#            }
    PAYPAL_PREFIX = "https://svcs.paypal.com/AdaptivePayments/"
    PAYPAL_HEADERS = {
           "X-PAYPAL-SECURITY-USERID" : "laurentenhoor_api1.gmail.com",
           "X-PAYPAL-SECURITY-PASSWORD" : "4WLJW9NSNS5U672X",
           "X-PAYPAL-SECURITY-SIGNATURE" : "AX0k7--E8124Zq8iDMqFDVJa3nx1AIeDzR8uHwsqZQ9IKNgZwrlhJspl",
           "X-PAYPAL-APPLICATION-ID" : "APP-4TV95696XM249222G",
           "X-PAYPAL-REQUEST-DATA-FORMAT" : "JSON",
           "X-PAYPAL-RESPONSE-DATA-FORMAT" : "JSON",
           }
    
    paypal_api_content = {
        "actionType" : "PAY",
#         "senderEmail" : sender,
        "receiverList" : {
            "receiver" : [{
                "email" : receiver,
                "amount" : str(amount),
                "paymentType" : "PERSONAL"
            }
#             ,{
#                 "email" : 'laurentenhoor@gmail.com',
#                 "amount" : "0.11",
#                 "paymentType" : "SERVICE"
#             }
        ]},
        "currencyCode" : "EUR",
        "cancelUrl" : "http://www.samsamsam.nl/",
        "returnUrl" : "http://www.samsamsam.nl/return_personal_payment/" + transaction_hash,
        "feesPayer" : "SENDER",
#         "clientDetails" : "ik ben een client!!",
        "memo" : description,
        "paymentType" : "PERSONAL",
        "payKeyDuration" : "P30D",
        "requestEnvelope" : {
            "errorLanguage" : "en_US",
            "detailLevel" : "ReturnAll",
        }, 
#         "applicationId" : "Samsamsamsamsam",
 
    }
    
    response = requests.post(PAYPAL_PREFIX + paypal_api, data=json.dumps(paypal_api_content), headers=PAYPAL_HEADERS)
    data = response.json()
    
    print(response)
    print(data)
    
    return data['payKey']
    
    
def cancel_payment(request):
    print('Cancelled Payment' + request.body)
    return HttpResponse(json.dumps({"id": 'this is me!'}), content_type="application/json")
    
def login_return(request):
    
    authCode = request.GET.get('code', '')
    
    if not authCode:
        return HttpResponseRedirect('/')
    
    # Create tokeninfo with Authorize code
    tokeninfo = Tokeninfo.create(authCode)
   
#     request.session['id_token'] = tokeninfo.id_token
    request.session['access_token'] = tokeninfo.access_token
    request.session['refresh_token'] = tokeninfo.refresh_token
    request.session['logout_url'] = tokeninfo.logout_url()
#     request.session.set_expiry(float(tokeninfo.expires_in))
    
    # Get userinfo
    userinfo = tokeninfo.userinfo()
    request.session['email'] = userinfo.email
    request.session['name'] = userinfo.name
    checkUser(userinfo.email, True)
    
    return afterLogin(request)


def logout(request):
    
    logout_url = request.session['logout_url']
    
    for key in request.session.keys():
        del request.session[key]
    
    return HttpResponseRedirect(logout_url)


def getStatus(paykey=''):
    
    PAYPAL_PREFIX = "https://svcs.paypal.com/AdaptivePayments/"
    PAYPAL_HEADERS = {
       "X-PAYPAL-SECURITY-USERID" : "laurentenhoor_api1.gmail.com",
       "X-PAYPAL-SECURITY-PASSWORD" : "4WLJW9NSNS5U672X",
       "X-PAYPAL-SECURITY-SIGNATURE" : "AX0k7--E8124Zq8iDMqFDVJa3nx1AIeDzR8uHwsqZQ9IKNgZwrlhJspl",
       "X-PAYPAL-APPLICATION-ID" : "APP-4TV95696XM249222G",
       "X-PAYPAL-REQUEST-DATA-FORMAT" : "JSON",
       "X-PAYPAL-RESPONSE-DATA-FORMAT" : "JSON",
    }
    
    paypal_api = "PaymentDetails"
    
    if paykey== '':
        paykey = "AP-4DE159689U7357042"
        
    paypal_api_content = {
        "payKey" : paykey,
        "requestEnvelope" : {
            "errorLanguage" : "en_US",
            "detailLevel" : "ReturnAll",
        }
    }
    
    response = requests.post(PAYPAL_PREFIX + paypal_api, data=json.dumps(paypal_api_content), headers=PAYPAL_HEADERS)
    data = response.json()
    print(data)
    
#    CREATED COMPLETED 
    return data['status']


def status(request, paykey):
    status = getStatus(paykey)
    return render(request, 'paypal/status.html', {"paykey": status})   
    

def paypal_return(request):
    print('IPN')
    
    received_json_data=json.loads(request.body)
    print(received_json_data)
    
    return HttpResponseRedirect('/')
    