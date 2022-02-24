from django.contrib import admin
from .models import Product,InvoiceItem,Invoice

@admin.register(Product)
class Admin(admin.ModelAdmin):
    list_display = ['id','product_name', 'unit_price', 'product_image', ]
    
@admin.register(Invoice)
class Admin(admin.ModelAdmin):
    list_display = ['invoice_number', 'customer_name', 'date_created','created_by', 'total']
@admin.register(InvoiceItem)
class Admin(admin.ModelAdmin):
    list_display = ['id','invoice', 'item','quantity','accumulated',]

