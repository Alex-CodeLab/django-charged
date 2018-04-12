from django.conf.urls import url
from .views import Info, Invoice, Invoices, Demo_page
from django.views.decorators.csrf import csrf_exempt

urlpatterns =[
    url(r'^info$', Info.as_view(), name='info'),
    url(r'^invoices/$', Invoices.as_view(), name='invoices'),
    url(r'^invoice/(?P<label>[a-zA-Z0-9]+)$', Invoice.as_view(), name='invoice_get'),
    url(r'^invoice$', csrf_exempt(Invoice.as_view()), name='invoice_create'),
    url(r'^demo', Demo_page.as_view(), name='demo_page'),
]
