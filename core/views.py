
from django.shortcuts import redirect, render
from .models import Product
from django.db import connection
from django.contrib import messages
from SalesManagementSystem.settings import MEDIA_ROOT
import os
from PIL import Image


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# Create your views here.
def products(request):
    q = request.GET.get('filter',None)
    products={}
    # if q is not None:
    #     products = Product.objects.raw('SELECT * FROM core_Product WHERE unit_price<%s and unit_price>0',[str(q)])
    # else:
    #     products = Product.objects.raw('SELECT * FROM core_Product WHERE unit_price>0')
        
    with connection.cursor() as cursor:
        if q is not None:
            cursor.execute('SELECT * FROM core_Product WHERE unit_price<=%s and unit_price>0',[str(q)])
        else:
            cursor.execute('SELECT * FROM core_Product WHERE unit_price>0')
        products = dictfetchall(cursor)
    context={
        'products':products,
        'q':q
    }
    return render(request,"core/products.html",context)

def productslistView(request):
    q = request.GET.get('search',None)
    products={}  
    with connection.cursor() as cursor:
        if q is not None:
            search = "%"+q+"%"
            cursor.execute("""SELECT * FROM core_Product WHERE lower(product_name) LIKE %s and product_name!="deleted product" """,[str(search)])
            print('here')
        else:
            cursor.execute('SELECT * FROM core_Product WHERE unit_price>0')
        products = dictfetchall(cursor)
    context={
        'products':products,
        'q':q
    }
    return render(request,"core/productslist.html",context)


            
def createproduct(request):
    if request.method == 'POST':
        f = request.FILES.get('product_image')
        path = os.path.join(MEDIA_ROOT,'products_pics',f.name)
        with open(path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        img = Image.open(path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(path)
        product_name = request.POST.get('product_name')
        unit_price = request.POST.get('unit_price')
        product_image = 'products_pics/'+request.FILES.get('product_image').name
        with connection.cursor() as cursor:
            cursor.execute('INSERT into core_Product (product_name,unit_price,product_image) values(%s,%s,%s)',[str(product_name),int(unit_price),str(product_image)])
        messages.success(request, f'{ product_name } added.')
    return render(request,"core/createproduct.html")
    
    
    
def createinvoice(request):
    return render(request,"core/createinvoice.html")