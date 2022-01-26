from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Product
from django.db import connection
from django.contrib import messages
from .helpers import dictfetchall,savefile,filterupdates


#views here.
def products(request):
    "retrieve view for products."
    q = request.GET.get('filter',None)
    products={}
    # if q is not None:
    #     products = Product.objects.raw('SELECT * FROM core_product WHERE unit_price<=%s and unit_price>0',[str(q)])
    # else:
    #     products = Product.objects.raw('SELECT * FROM core_product WHERE unit_price>0')
    with connection.cursor() as cursor:
        if q is not None:
            cursor.execute('SELECT * FROM core_product WHERE unit_price<=%s and unit_price>0',[str(q)])
        else:
            cursor.execute('SELECT * FROM core_product WHERE unit_price>0')
        products = dictfetchall(cursor)
    context={
        'products':products,
        'q':q
    }
    return render(request,"core/products.html",context)

def productslistView(request):
    "list view for products."
    q = request.GET.get('search',None)
    products={}  
    with connection.cursor() as cursor:
        if q is not None:
            search = "%"+q+"%"
            cursor.execute("""SELECT * FROM core_product WHERE lower(product_name) LIKE %s and product_name!="deleted product" """,[str(search)])
        else:
            cursor.execute('SELECT * FROM core_product WHERE unit_price>0')
        products = dictfetchall(cursor)
    context={
        'products':products,
        'q':q
    }
    return render(request,"core/productslist.html",context)

def createproduct(request):
    "create view for products."
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        unit_price = request.POST.get('unit_price')
        f = request.FILES.get('product_image')
        product_image = 'products_pics/'+savefile(f,'products_pics')
        with connection.cursor() as cursor:
            cursor.execute('INSERT into core_product (product_name,unit_price,product_image) values(%s,%s,%s)',[str(product_name),int(unit_price),str(product_image)])
        messages.success(request, f'{ product_name } added.')
    return render(request,"core/createproduct.html")

def updateproduct(request,pk):
    "update view for product for given pk"
    product={}
    fields = { 'normal_fields':['product_name','unit_price',],'file_fields':['product_image']}
    dir = 'products_pics/'
    
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute('select * from core_product where id = %s',[int(pk)])
            product = dictfetchall(cursor)
            
        (filtered_dict,text_field_updated_flag,file_field_updated_flag)=filterupdates(request,product,fields,dir)
        updated_text_fields= filtered_dict['updated_text_fields']
        updated_file_fields = filtered_dict['updated_file_fields']
        
        if text_field_updated_flag : 
            for field,value in updated_text_fields.items():
                query = f'UPDATE core_product SET {field} = %s WHERE id = {pk} '
                with connection.cursor() as cursor:
                    cursor.execute(query,[value])
                    
        if file_field_updated_flag :
            for field,value in updated_file_fields.items():
                print(field,value,type(value))
                f = request.FILES.get(field)
                filepath = 'products_pics/'+savefile(f,'products_pics')
                query = f'UPDATE core_product SET {field} = %s WHERE id = {pk} '
                with connection.cursor() as cursor:
                    cursor.execute(query,[filepath])
                
        product_name = product[0].get('product_name')
        reverseurl = reverse('updateproduct',kwargs={'pk': pk})
        
        if not text_field_updated_flag and not file_field_updated_flag:
            messages.info(request, f'{ product_name} has no new updates.')
            return redirect(reverseurl)
        
        messages.success(request, f'{ product_name} updated.')
        return redirect(reverseurl)

    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute('select * from core_product where id = %s',[int(pk)])
            product = dictfetchall(cursor)
        context={
        'products':product,
        'pk':pk,
        }
        return render(request,"core/updateproduct.html",context)    


def createinvoice(request):
    return render(request,"core/createinvoice.html")