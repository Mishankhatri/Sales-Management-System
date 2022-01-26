from django.urls import path
from . import views

urlpatterns = [
    path("", views.products, name="products"),
    path("productlist/", views.productslistView, name="productslist"),
    path("createinvoice/", views.createinvoice, name="createinvoice"),
    path("createproduct/", views.createproduct, name="createproduct"),
    path("products/<int:pk>/update/", views.updateproduct, name="updateproduct"),
    # path("product/<int:pk>/delete", views.deleteproduct, name="deleteproduct"),
    ]