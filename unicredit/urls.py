from django.conf.urls.defaults import *
from unicredit import views


urlpatterns = patterns('',
    url(r'^redirect/', views.PaymentView.as_view(), name='unicredit-direct-payment'),
    url(r'^listener-payment/', views.ListenerPayment.as_view(), name='unicredit-listener-payment'),
    url(r'^thank-you/', views.ThankYouView.as_view(), name='unicredit-confirm-response'),
    url(r'^cancel/', views.CancelResponseView.as_view(), name='unicredit-cancel-response'),
)
