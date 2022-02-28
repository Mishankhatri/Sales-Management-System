from .models import Invoice,InvoiceItem
from django.forms.models import inlineformset_factory

InvoiceFormSet = inlineformset_factory(Invoice,InvoiceItem,fields=('item','quantity',),extra=5,can_delete=False)