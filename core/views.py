from django.shortcuts import render

# Create your views here.
def products(request):
    return render(request,"core/products.html")

def createinvoice(request):
    return render(request,"core/createinvoice.html")