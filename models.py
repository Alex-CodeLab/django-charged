from django.db import models
from django.conf import settings
from lightning import LightningRpc
from datetime import datetime, timezone


class Invoice(models.Model):
    label           = models.CharField(max_length=128, blank=False, unique=True)
    msatoshi        = models.BigIntegerField(null=False)
    quoted_currency = models.CharField(max_length=4, null=True, verbose_name='currency')
    quoted_amount   = models.DecimalField(decimal_places=3,max_digits=20, null=True, verbose_name='amount')
    rhash           = models.CharField(max_length=300, blank=False, unique=True) # payment_hash
    payreq          = models.CharField(max_length=1000, blank=False) # bolt11
    status          = models.CharField(max_length=128, default='unpaid') #'unpaid', 'paid' or 'expired'
    pay_index       = models.IntegerField(null=True, blank=True)
    description     = models.CharField(max_length=640, blank=False)
    metadata        = models.TextField(blank=True, default='')
    created_at      = models.DateTimeField(auto_now_add=True, auto_now=False)
    expires_at      = models.DateTimeField(null=True, blank=True)
    paid_at         = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.label)

    def satoshi(self):
        return round(self.msatoshi / 1000)

    def amount(self):
        if self.quoted_amount and self.quoted_currency :
            return str(round(self.quoted_amount, 2)) + ' ' + self.quoted_currency

    def current_status(self):
        if self.status == "unpaid":
            try:
                inv = LightningRpc(settings.LIGHTNING_RPC).listinvoices(self.label)

                inv_ln = inv['invoices'][0]
                if inv_ln['status'] == "expired":
                    self.status = inv_ln['status']
                if inv_ln['status'] == "paid":
                    self.status = inv_ln['status']
                    self.paid_at = datetime.fromtimestamp(inv_ln['paid_at'], timezone.utc)
                    self.pay_index = inv_ln['pay_index']
                self.save()
                return self.status
            except:
                return '-'
        else:
            return self.status