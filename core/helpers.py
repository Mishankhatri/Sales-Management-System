import os,string,random
from SalesManagementSystem.settings import MEDIA_ROOT
from PIL import Image

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