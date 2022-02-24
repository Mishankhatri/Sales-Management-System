from django.urls import path
from . import views

urlpatterns = [
    path("", views.products, name="products"),
    path("productlist/", views.productslistView, name="productslist"),
    path("createinvoice/", views.createinvoice, name="createinvoice"),
    path("createproduct/", views.createproduct, name="createproduct"),
    path("sales/", views.sales, name="sales"),
    path("products/<int:pk>/update/", views.updateproduct, name="updateproduct"),
    path("product/<int:pk>/delete/", views.deleteproduct, name="deleteproduct"),
    path("addinvoiceitems/<int:pk>/", views.addinvoiceitems, name="addinvoiceitems"),
    path("invoices/<int:invoice_number>/deleteitem/<int:item_pk>/", views.deleteinvoiceitem, name="deleteinvoiceitem"),
    path("invoices/<int:pk>/delete/", views.deleteinvoice, name="deleteinvoice"),
    path("invoices/<int:pk>/details/", views.invoicedetail, name="invoice_details"),
    path("invoices/<int:pk>/print/", views.printinvoice, name="print_invoice"),
    ]