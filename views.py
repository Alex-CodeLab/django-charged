import json

from django.views import View
from django.views.generic import TemplateView
from .decorators import local_only
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from .api import Ln
from .utils import rndstr, exchange_rate


@method_decorator(local_only, name='get')
class Info(View):
    def get(self, request):
        result = Ln().getinfo()

        if result:
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            return JsonResponse({'error': 'error'})



@method_decorator(local_only, name='get')
class Invoice(View):
    btc_msat_ratio = 100000000000

    def post(self, request):

        params = {}
        options = ['amount', 'msatoshi', 'description', 'currency', 'expiry']

        for option in options:
            params[option] = request.POST.get(option)

        params['label'] = rndstr()

        try:
            if params['amount'] is not None and params['currency'] is not None:
                exch_rate = exchange_rate(params['currency'])
                params['msatoshi'] = round(float(params['amount']) / exch_rate * self.btc_msat_ratio)
        except:
            return JsonResponse({'error': 'conversion error'})

        try:
            if params['label'] is None or params['description'] is None:
                return JsonResponse({'error': 'missing arguments_'})
        except KeyError:
            return JsonResponse({'error': 'missing arguments'})

        try:
            result = Ln().invoice_create(params=params)
            if result:
                return HttpResponse(json.dumps(result), status=201, content_type='application/json')
            return JsonResponse({'error': 'missing arguments__'})
        except:
            return JsonResponse({'error': 'error'})



    def get(self,request,label):
        params = {'label': label}
        result = Ln().invoice_get(params=params)
        if result is not False:
            return HttpResponse(json.dumps(result), content_type='application/json')



@method_decorator(local_only, name='get')
class Invoices(View):

    def get(self, request):
        try:
            result = Ln().invoiceslist()
            return HttpResponse(result, content_type='application/json')
        except:
            return JsonResponse({'error': 'error'})



class registerlistener(View):
    pass


class Demo_page(TemplateView):
    template_name = 'demo_page.html'

