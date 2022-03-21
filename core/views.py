from datetime import datetime
from django.shortcuts import redirect, render
import os
from SalesManagementSystem.settings import MEDIA_ROOT
from .forms import InvoiceFormSet
from .models import Invoice
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .helpers import deletefile, dictfetchall, render_to_pdf,savefile,filterupdates,getInvoiceDetails


#views here.
def products(request):
    "retrieve view for products."
    q = request.GET.get('filter',None)
    products={}
    #using django's model manager metod - raw()
    # if q is not None:
    #     products = Product.objects.raw('SELECT * FROM core_product WHERE unit_price<=%s and unit_price>0',[str(q)])
    # else:
    #     products = Product.objects.raw('SELECT * FROM core_product WHERE unit_price>0')
    with connection.cursor() as cursor:
        if q is not None:
            cursor.execute('SELECT * FROM core_product WHERE unit_price<=%s and unit_price>0 order by product_name',[str(q)])
        else:
            cursor.execute('SELECT * FROM core_product WHERE unit_price>0 order by product_name')
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
            cursor.execute("""SELECT * FROM core_product WHERE lower(product_name) LIKE %s and product_name!="deleted product" order by product_name""",[str(search)])
        else:
            cursor.execute('SELECT * FROM core_product WHERE unit_price>0 order by product_name')
        products = dictfetchall(cursor)
    context={
        'products':products,
        'q':q
    }
    return render(request,"core/productslist.html",context)

@login_required
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

@login_required
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
                f = request.FILES.get(field)
                filepath = 'products_pics/'+savefile(f,'products_pics')
                query = f'UPDATE core_product SET {field} = %s WHERE id = {pk} '
                with connection.cursor() as cursor:
                    cursor.execute(query,[filepath])
                
        product_name = product[0].get('product_name')
        
        if not text_field_updated_flag and not file_field_updated_flag:
            messages.info(request, f'{ product_name} has no new updates.')
            return redirect('updateproduct',pk=pk)
        
        messages.success(request, f'{ product_name} updated.')
        return redirect('updateproduct',pk=pk)

    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute('select * from core_product where id = %s',[int(pk)])
            product = dictfetchall(cursor)
        context={
        'products':product,
        'pk':pk,
        }
        return render(request,"core/updateproduct.html",context)    

@login_required
@user_passes_test(lambda u: u.is_superuser)
def deleteproduct(request,pk):
    "delete view for product for given pk"
    product= {}
    with connection.cursor() as cursor:
        cursor.execute('select * from core_product where id = %s',[int(pk)])
        product = dictfetchall(cursor)
    product_name = product[0].get('product_name')

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(' DELETE FROM core_product WHERE id = %s',[int(pk)])
        product_image = product[0].get('product_image')
        path = os.path.join(MEDIA_ROOT,product_image)
        deletefile(path)
        messages.success(request, f'{ product_name } Deleted.')
        return redirect('products')

    if request.method == 'GET':
        context= {
            'product' : product
        }
        return render(request,"core/product_confirm_delete.html",context)    

@login_required
def createinvoice(request):
    "create view for invoice."
    if request.method == 'POST':
        current_pk = 0
        created_by_id = request.user.id
        customer_name = request.POST.get('customer_name')
        date_created = datetime.now()
        with connection.cursor() as cursor:
            cursor.execute('INSERT into core_invoice (customer_name,created_by_id,date_created,total) values(%s,%s,%s,%s)',[str(customer_name),int(created_by_id),date_created,0])
            current_pk = cursor.lastrowid
        messages.success(request, f'Invoice created for { customer_name }.')
        return redirect('addinvoiceitems',pk=current_pk)
    return render(request,"core/createinvoice.html")

@login_required
@user_passes_test(lambda u: u.is_superuser)
def deleteinvoice(request,pk):
    "delete view for invoice for given pk"
    invoice= None
    with connection.cursor() as cursor:
        cursor.execute('select * from core_invoice where invoice_number = %s',[int(pk)])
        invoice = dictfetchall(cursor)[0]
    customer_name = invoice.get('customer_name')

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(' DELETE FROM core_invoice WHERE invoice_number = %s',[int(pk)])
        messages.success(request, f'Invoice for { customer_name } deleted.')
        return redirect('sales')

    if request.method == 'GET':
        context= {
            'invoice' : invoice
        }
        return render(request,"core/invoice_confirm_delete.html",context)  


@login_required
def addinvoiceitems(request,pk):
    "add invoiceitms view on invoice."
    form = InvoiceFormSet()
    context={
        'form':form,
        'pk':pk
    }
    getInvoiceDetails(pk,context)
    if request.method == 'POST':
        form = InvoiceFormSet(request.POST,instance=Invoice.objects.get(invoice_number=pk))
        total = 0
        if form.is_valid():
            for data in form.cleaned_data:
                if data:
                    cleaned_dict={}
                    item = data.get('item')
                    for k,v in data.items():
                        try:
                            if v.pk:
                                cleaned_dict[k]=v.pk
                        except:
                            cleaned_dict[k]=v
                    item_id = cleaned_dict['item']
                    unit_price = item.unit_price
                    quantity = cleaned_dict['quantity']
                    accumulated = unit_price*quantity
                    with connection.cursor() as cursor:
                        cursor.execute('INSERT into core_invoiceitem (quantity,accumulated,invoice_id,item_id) values(%s,%s,%s,%s)',[int(quantity),int(accumulated),pk,int(item_id)])
            with connection.cursor() as cursor:
                cursor.execute('select sum(accumulated) as total from core_invoiceitem where invoice_id = %s ',[int(pk)])
                total = cursor.fetchone()[0]
                cursor.execute('update core_invoice set total = %s where invoice_number = %s',[int(total),int(pk)])
            getInvoiceDetails(pk,context)
    return render(request,"core/additemstoinvoice.html",context)

@login_required
def deleteinvoiceitem(request,item_pk,invoice_number):
    "delete view for invoiceitem for given pk and invoice_number."
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM core_invoiceitem WHERE id = %s',[int(item_pk)])
            messages.success(request, 'Item deleted.')
        with connection.cursor() as cursor:
            cursor.execute('select sum(accumulated) as total from core_invoiceitem where invoice_id = %s ',[int(invoice_number)])
            total = cursor.fetchone()[0]
            cursor.execute('update core_invoice set total = %s where invoice_number = %s',[int(total),int(invoice_number)])
        return redirect('addinvoiceitems',pk=invoice_number)

@login_required
def invoicedetail(request,pk):
    "detail view for invoice."
    if request.method == 'GET':
        context={}
        getInvoiceDetails(pk,context)
        return render(request,"core/invoicedetails.html",context)

@login_required
def sales(request):
    "sales view for invoices."
    if request.method == 'GET':
        q = request.GET.get('search',None) 
        context={}
        invoices_dict=None
        with connection.cursor() as cursor:
            if q is not None:
                search = "%"+q+"%"
                cursor.execute('select core_invoice.invoice_number,core_invoice.customer_name,core_invoice.date_created,core_invoice.total,auth_user.username as created_by from core_invoice inner join auth_user on core_invoice.created_by_id = auth_user.id WHERE core_invoice.customer_name LIKE %s ',[str(search)])
            else:
                cursor.execute('select core_invoice.invoice_number,core_invoice.customer_name,core_invoice.date_created,core_invoice.total,auth_user.username as created_by from core_invoice inner join auth_user on core_invoice.created_by_id = auth_user.id order by core_invoice.date_created desc ')
            invoices_dict = dictfetchall(cursor)
        context['invoices_dict']=invoices_dict
        context['q']=q
        return render(request,"core/sales.html",context)

@login_required
def printinvoice(request,pk):
    "print invoice view for given pk."
    if request.method == 'GET':
        context={}
        getInvoiceDetails(pk,context)
        pdf = render_to_pdf('core/invoice_print.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

