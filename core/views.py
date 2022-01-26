from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Product
from django.db import connection
from django.contrib import messages
from SalesManagementSystem.settings import MEDIA_ROOT
import os,string,random
from PIL import Image


#utility function
def dictfetchall(cursor):
    "Return all rows from a cursor as a list of dicts"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
def savefile(file,dir):
    "returns saved file path after saving the uploaded file from client,Takes <UploadedFile> and <str>directory to save file inside MEDIA ROOT"
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 6)) 
    filename = random_string+file.name 
    path = os.path.join(MEDIA_ROOT,dir,filename)
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    img = Image.open(path)
    if img.height > 300 or img.width > 300:
        output_size = (300,300)
        img.thumbnail(output_size)
        img.save(path)
    return filename

def control_datatype(stg):
        "returns integer from string if exists else returns string"
        clean = stg
        try:
            clean = int(stg.strip(string.ascii_letters))
        finally:
            return clean
        
def filterupdates(request,instance,fields,dir):
    "returns tuple of filtered dict ,text_field_updated flag and file_field_updated flag. Takes request,instance,fields and file-upload directory,expected <format> fields = { 'normal_fields':['normal_field_names',],'file_fields':['file_field_names']} "
    normal_fields = fields['normal_fields']
    file_fields = fields['file_fields']
    prev_dict = {}
    updated_dict= {}
    updated_text_fields={}
    updated_file_fields={}
    text_updated_flag = False
    file_updated_flag = False 
            
    for n_field in normal_fields:
        prev = f'prev_{n_field}'
        updated = f'{n_field}'
        prev_dict[prev] = instance[0].get(n_field)
        if str(prev_dict.get(prev)) != request.POST.get(n_field): #request.POST is of type QueryDict and .get() returns <str> of provided key
            updated_text_fields[updated] = control_datatype(request.POST.get(n_field))
            
    for f_field in file_fields:
        prev = f'prev_{f_field}'
        updated = f'{f_field}'
        prev_dict[prev] = instance[0].get(f_field)
        if request.FILES.get(f_field) is not None and str(prev_dict.get(prev)) != dir+request.FILES.get(f_field).name:
            updated_file_fields[updated] = dir+request.FILES.get(f_field).name
    
    updated_dict['updated_text_fields']= updated_text_fields
    updated_dict['updated_file_fields']= updated_file_fields
    
    if updated_text_fields: text_updated_flag = True
    if updated_file_fields: file_updated_flag = True
    return (updated_dict,text_updated_flag,file_updated_flag)

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
            print('here')
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
        f = request.FILES.get('product_image')
        path = os.path.join(MEDIA_ROOT,'products_pics',f.name)
        with open(path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        img = Image.open(path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            print('reducing....')
            img.save(path)
        product_name = request.POST.get('product_name')
        unit_price = request.POST.get('unit_price')
        product_image = 'products_pics/'+request.FILES.get('product_image').name
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
        if not text_field_updated_flag and not file_field_updated_flag:
            messages.info(request, f'{ product_name} has no new updates.')
            reverseurl = reverse('updateproduct',kwargs={'pk': pk})
            return redirect(reverseurl)
        messages.success(request, f'{ product_name} updated.')
        return redirect('products')
            
    #     print(product)
    #     prev_name = product[0].get("product_name")
    #     prev_price = product[0].get("unit_price")
    #     prev_img = product[0].get("product_image")
    #     print(prev_name,prev_price,prev_img)
    #     product_name = request.POST.get('product_name')
    #     unit_price = request.POST.get('unit_price')
    #     if request.FILES.get('product_image') is None:
    #         product_image = prev_img
    #     else:
    #         product_image = 'products_pics/'+request.FILES.get('product_image').name
    #         f = request.FILES.get('product_image')
    #         path = os.path.join(MEDIA_ROOT,'products_pics',f.name)
    #         with open(path, 'wb+') as destination:
    #             for chunk in f.chunks():
    #                 destination.write(chunk)
    #         img = Image.open(path)
    #         if img.height > 300 or img.width > 300:
    #             output_size = (300,300)
    #             img.thumbnail(output_size)
    #             img.save(path)
    #     print(product_name,unit_price,product_image)
    #     changed_fields={}
    #     if prev_name != product_name: 
    #         changed_fields.update({"product_name":product_name})
    #     if int(prev_price) != int(unit_price): 
    #         changed_fields.update({"unit_price":int(unit_price)})
    #     if prev_img != product_image:
    #         changed_fields.update({"product_image":product_image})
    #     print(changed_fields)
    #     for field,value in changed_fields.items():
    #         print(field,value)
    #         with connection.cursor() as cursor:
    #             cursor.execute('UPDATE core_product set "%s" = "%s" WHERE id = %s',[str(field),value,int(pk)])
            
    #     f = request.FILES.get('product_image')
    #     path = os.path.join(MEDIA_ROOT,'products_pics',f.name)
    #     with open(path, 'wb+') as destination:
    #         for chunk in f.chunks():
    #             destination.write(chunk)
    #     img = Image.open(path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(path)
        # product_name = request.POST.get('product_name')
        # unit_price = request.POST.get('unit_price')
        # product_image = 'products_pics/'+request.FILES.get('product_image').name
    #     with connection.cursor() as cursor:
    #         cursor.execute('UPDATE core_product set product_name = %s, unit_price = %s,product_image= %s, WHERE id = %s',[str(product_name),int(unit_price),str(product_image),int(product_id)])
        # messages.success(request, f'{ product_name } updated.')
        # return redirect('products')
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