import os,string,random
from SalesManagementSystem.settings import MEDIA_ROOT
from django.db import connection
from PIL import Image
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    "renders html_template to pdf as HttpResponse given template_src and context_dict"
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

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

def deletefile(path):
    "deletes the file from given path."
    if os.path.isfile(path):
        os.remove(path)
        print(f'file deleted from {path}')
    else : print ( "File not found...")

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

def getInvoiceDetails(pk,context):
    "adds invoice details and invoice_items views to the context of particular pk"
    invoice_dict = None
    invoice_items = None
    with connection.cursor() as cursor:
        cursor.execute('select core_invoice.invoice_number,core_invoice.customer_name,core_invoice.date_created,core_invoice.total,auth_user.username as created_by from core_invoice inner join auth_user on core_invoice.created_by_id = auth_user.id where invoice_number = %s ',[int(pk)])
        invoice_dict = dictfetchall(cursor)[0]
    with connection.cursor() as cursor:
        cursor.execute('select core_invoiceitem.id,core_product.product_name,core_product.unit_price,core_invoiceitem.quantity,core_invoiceitem.accumulated from ((core_invoice inner join core_invoiceitem on core_invoice.invoice_number=core_invoiceitem.invoice_id ) inner join core_product on core_invoiceitem.item_id = core_product.id) where invoice_number = %s ',[int(pk)])
        invoice_items = dictfetchall(cursor)
    context['invoice_dict'] = invoice_dict
    context['invoice_items'] = invoice_items