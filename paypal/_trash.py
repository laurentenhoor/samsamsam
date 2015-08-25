def create_bill(request):
    
    totalAmount = float(request.POST.get('amount'))
    
    user = checkUser(request.session['email'])
    user.save()
    bill = user.bill_set.create(
                                amount=totalAmount,
                                description=request.POST.get('description'),
                                user=user,
                                status="Created"
                                )
    bill.save()
    request.session['bill_id'] = bill.id
    
    transaction_emails = request.POST.getlist('emaillist')
    
    splittedAmount = totalAmount / len(transaction_emails)
    
    for email in transaction_emails:
    
        transaction_user = checkUser(email)
        bill.transaction_set.create(
                                    user=transaction_user,
                                    amount=splittedAmount,
                                    status="Unpaid",
                                    )
    
    payKey = getTransactionPaykey()
    bill.paykey = payKey
    
    bill.save()
    
    return render(request, 'paypal/create_bill.html', {'bill': bill})




def getTransactionPaykey():
    
    paypal_api = "Pay";
    
    paypal_api_content = {
        "actionType" : "PAY",
        "receiverList" : {
            "receiver" : [{
                "email" : "payment@samsamsam.nl",
                "amount" : "0.24",
                "paymentType" : "DIGITALGOODS",
            }]
        },
        "currencyCode" : "EUR",
        "cancelUrl" : "http://beta.samsamsam.nl/",
        "returnUrl" : "http://beta.samsamsam.nl/",
        "paymentType" : "DIGITALGOODS",
        "requestEnvelope" : {
            "errorLanguage" : "en_US",
            "detailLevel" : "ReturnAll",
        }
    }
    
    response = requests.post(PAYPAL_PREFIX + paypal_api, data=json.dumps(paypal_api_content), headers=PAYPAL_HEADERS)
    data = response.json()
    
    return data['payKey']
    
    
    
def personal_payment(request):
    
    paypal_api = "Pay";
    
    # Adaptive payments
    PAYPAL_PREFIX = "https://svcs.sandbox.paypal.com/AdaptivePayments/"
    PAYPAL_HEADERS = {
           "X-PAYPAL-SECURITY-USERID" : "laurentenhoor-facilitator_api1.gmail.com",
           "X-PAYPAL-SECURITY-PASSWORD" : "1403877035",
           "X-PAYPAL-SECURITY-SIGNATURE" : "AFcWxV21C7fd0v3bYYYRCpSSRl31AnxMpEgWsQEZ1e7xxrMOYanv5NV8",
           "X-PAYPAL-APPLICATION-ID" : "APP-80W284485P519543T",
           "X-PAYPAL-REQUEST-DATA-FORMAT" : "JSON",
           "X-PAYPAL-RESPONSE-DATA-FORMAT" : "JSON",
           }
    
    
    paypal_api_content = {
        "actionType" : "PAY",
        "receiverList" : {
            "receiver" : [{
                "email" : "donenad@live.nl",
                "amount" : "2.50"
            }, {
                "email" : "adrianus@gmail.com",
                "amount" : "5.50"
            }]
        },
        "currencyCode" : "EUR",
        # "senderEmail" : "laurentenhoor@gmail.com", # Do not determine payer! Not working!
        "cancelUrl" : "http://beta.samsamsam.nl/",
        "returnUrl" : "http://beta.samsamsam.nl/",
        "paymentType" : "PERSONAL",
#         "useCredentials" : "true", # Not sure about this
        # preapprovalKey : preapprovalKey,
        "requestEnvelope" : {
            "errorLanguage" : "en_US",
            "detailLevel" : "ReturnAll",
        }
    }
    
    response = requests.post(PAYPAL_PREFIX + paypal_api, data=json.dumps(paypal_api_content), headers=PAYPAL_HEADERS)
    data = response.json()
    
    cgi = 'https://www.paypal.com/cgi-bin/webscr?cmd=_ap-payment&paykey='
    webapps = 'https://www.sandbox.paypal.com/webapps/adaptivepayment/flow/pay?paykey='
    urlPrefix = webapps
    
    return render(request, 'paypal/personal_payment.html', {'payKey' : data['payKey']})
#     return HttpResponseRedirect(urlPrefix + data['payKey'])

