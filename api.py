import json
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timezone
from .models import Invoice
from lightning import LightningRpc


class Ln(LightningRpc):

    def __init__(self, *args, **kwargs):
        super(Ln, self).__init__(settings.LIGHTNING_RPC)


    def invoice_create(self, params):
        invoice = self.invoice(params['msatoshi'], params['label'], params['description'], params['expiry'])

        Invoice.objects.create(rhash=invoice['payment_hash'],
                               msatoshi=params['msatoshi'],
                               label=params['label'],
                               expires_at=datetime.fromtimestamp(invoice['expires_at'], timezone.utc),
                               description=params['description'],
                               payreq=invoice['bolt11'],
                               quoted_amount=params['amount'],
                               quoted_currency=params['currency'])
        return invoice

    def invoice_get(self, params):
        try:
            invoice = Invoice.objects.get(label=params['label'])
            if invoice.status == "unpaid":
                inv = self.listinvoices(params['label'])
                inv_ln = inv['invoices'][0]

                if inv_ln['status'] == "expired":
                    invoice.status = inv_ln['status']
                if inv_ln['status'] == "paid":
                    invoice.status = inv_ln['status']
                    invoice.paid_at = datetime.fromtimestamp(inv_ln['paid_at'], timezone.utc)
                    invoice.pay_index = inv_ln['pay_index']
                invoice.save()
                return inv_ln
        except ObjectDoesNotExist:
            return False


    def invoices_list(self):
        invoices_json = serializers.serialize('json', Invoice.objects.all(), fields=('label','msatoshi','rhash','status'))
        invoices = json.loads(invoices_json)
        for invoice in invoices:
            del invoice['pk']
            del invoice['model']
            invoice['invoice'] = invoice.pop('fields')
        return json.dumps(invoices)


    def invoice_wait(self, params):
        invoice = Invoice.objects.get(rhash=params['payment_hash'])
        return self.waitinvoice(invoice.label)

