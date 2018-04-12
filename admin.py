from django.contrib import admin
from .models import Invoice


class InvoiceAdmin(admin.ModelAdmin):
    model = Invoice
    list_display = ['label', 'satoshi', 'amount',  'created_at', 'current_status']
    readonly_fields = ['label', 'satoshi', 'amount', 'status', 'created_at', 'rhash','msatoshi','payreq', 'description', 'metadata' , 'quoted_amount','quoted_currency', 'expires_at', 'paid_at', 'pay_index' ]



admin.site.register(Invoice, InvoiceAdmin)
