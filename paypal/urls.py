from django.conf.urls import url

from . import views

urlpatterns = [
               
    url(r'^$', views.login, name='login'),
    
    url(r'^save_bill/$', views.save_bill, name='save_bill'),
    url(r'^save_bill/(\d+)/$', views.save_bill, name='save_bill'),
    
    url(r'^delete_bill/(\d+)/$', views.delete_bill, name='delete_bill'),
    
    url(r'^rekening/$', views.new_bill, name='input_bill'),
    url(r'^edit_bill/(\d+)/$', views.edit_bill, name='edit_bill'),
    url(r'^login_return/$', views.login_return, name='login_return'),
    url(r'^payment_do/$', views.payment_do, name='payment_do'),
    
    url(r'^reminder/(\d+)/$', views.reminder, name='reminder'),
    
    url(r'^betalen/$', views.payments, name='payments'),
    url(r'^ontvangen/$', views.overview, name='overview'),
    
    url(r'^email_template/$', views.email_template, name='email_template'),
    
    url(r'^login_as/(?P<email>[^/]+)/$', views.login_as, name='login_as'),
    
    
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^status/(?P<paykey>[^/]+)/$', views.status, name='status'),
#     url(r'^status/$', views.status, name='status'),
    url(r'^seamless/(\d+)/$', views.seamless, name='seamless'),
    
    url(r'^return_email/(?P<transaction_hash>[^/]+)/$', views.return_email, name='return_email'),
    url(r'^return_personal_payment/(?P<transaction_hash>[^/]+)/$', views.return_personal_payment, name='return_personal_payment'),
    url(r'^privacy_policy/$', views.policies, name='privacy_policy'),
    url(r'^user_agreement/$', views.policies, name='user_agreement'),
    
    url(r'^paypal_return/$', views.paypal_return, name='paypal_return'),
    
    url(r'^construction/$', views.construction, name='construction'),
    
    url(r'^cancel_payment/$', views.cancel_payment, name='cancel_payment'),
   
    
    url(r'^REST/user/(?P<email>[^/]+)/$', views.user, name='user'),
    url(r'^REST/user/delete/(?P<email>[^/]+)/$', views.user_delete, name='user_delete'),
    url(r'^REST/user/$', views.user, name='user'),
    
    url(r'^mass_pay/$', views.mass_pay, name='mass_pay'),
    
]


