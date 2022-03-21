<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="media\sms.png" alt="Project logo"></a>
</p>

# <div align= "center"> Sales Management System</div>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)]()
</div>

---

<p align="center"> A database management system based project.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Features](#features)
- [Getting Started](#getting_started)
- [Built Using](#built_using)
- [Authors](#authors)
- [Quick Preview](#preview)

<br>

## 🧐 About <a name = "about"></a>
This is an admin based dbms web project developed for the management of the records of product, billing and product sales. It is created with the motive of creating ease for the counter-management side of any seller.


<br>


## ✨ Features <a name = "features"></a>

### For Registered Users :

- Admin Mode
   - Admin can register new staff.
   - Admin can CREATE, RETRIEVE, UPDATE and DELETE products.
   - Admin can CREATE, RETRIEVE, UPDATE, PRINT and DELETE invoices.

<br>

- Staff Mode
   - Staff can CREATE, RETRIEVE, UPDATE and DELETE products.
   - Staff can CREATE, RETRIEVE, UPDATE and PRINT invoices.
     
<br>

### For Unregistered users :
- Normal mode:
   - Can only view products list.


<br>

## 🏁 Getting Started <a name = "getting_started"></a>

- Clone the repository or download the zip file

- For zip file extract it, then cd into the directory 

- Create new virtualenv using python's [virtualenv](https://pypi.org/project/virtualenv/) package:

    ```
    $ virtualenv venv

    $ venv\Scripts\activate (in windows) or $source venv/bin/activate (in Mac OS/linux)

    ```

- Install all dependencies by executing the following command:

    ```
    $pip install -r requirements.txt
    ```

- Connect a MySQL database:
    >For development environment:
    <br>
    In **SalesManagementSystem/settings.py** replace the following code snippet according to your mysql database.
    ```
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<databasename>',
        'USER': '<username>',
        'PASSWORD': '<password>',
        'HOST': 'localhost',
        'PORT': '3306',
        }
    }
    ```

- For running the application simply execute the following commands:

    ```
    $python manage.py migrate
    $python manage.py runserver
    ```

- If you want to populate database with dummy data as shown in preview:
    ```
    $python manage.py loaddata sms.json
    ```

- For login you can use username/password from
    [dummyUsers.txt](./dummyUsers.txt) file
    assuming you loaded sms.json <br>or<br> to create new superuser execute:

    ```
    $python manage.py createsuperuser
    ```
- You can now login to the system!

- Now you can use the app by visiting [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

<br>

## ⛏️ Built Using <a name = "built_using"></a>

- [TailwindCSS](https://tailwindcss.com) - CSS Framework
- [Undraw.co](https://undraw.co/) - Open Source Illustrations
- [Django](https://www.djangoproject.com) - Web Framework

    >**Note** : In this project, Django's builtin  database-abstraction API is not used . All the create, insert, retrieve, update and delete operations of objects are done through embedded **raw SQL**.
- [MySQL](https://www.mysql.com/) - Relational Database

<br>

## ✍️ Authors <a name = "authors"></a>

- [@MishanKhatri](https://github.com/Mishankhatri)

<br>

## 👀 Quick Preview <a name = "preview"></a>

 - Homepage 
<p align="">
 <img width=auto height=auto src="media\PreviewPages\products.png" alt="#"></a>
</p>

 - Login 
<p align="">
 <img width=auto height=auto src="media\PreviewPages\login.png" alt="#"></a>
</p>

 - Products-list 
<p align="">
 <img width=auto height=auto src="media\PreviewPages\productlist.png" alt="productlist"></a>
</p>

 - Create Invoice 
<p align="">
 <img width=auto height=auto src="media\PreviewPages\createinvoice1.png" alt="createinvoice"></a>
</p>

 - Add Items to Invoice
<p align="">
 <img width=auto height=auto src="media\PreviewPages\additemstoinvoice.png" alt="additemstoinvoice"></a>
</p>

 - Print Invoice as Pdf 
<p align="">
 <img width=auto height=auto src="media\PreviewPages\invoiceprint.png" alt="#"></a>
</p>

 - Dashboard For Admin 
<p align="">
 <img width=auto height=auto src="media\PreviewPages\dashboard(admin).png" alt="#"></a>
</p>

 - Dashboard For Staff 
<p align="">
 <img width=auto height=auto src="media\PreviewPages\dashboard(staff).png" alt="#"></a>
</p>

 - Update Profile
<p align="">
 <img width=auto height=auto src="media\PreviewPages\updateprofile.png" alt="#"></a>
</p>

 - Add product to Database 
<p align="">
 <img width=auto height=auto src="media\PreviewPages\addproduct.png" alt="#"></a>
</p>

 - Delete product from Database 
<p align="">
 <img width=auto height=auto src="media\PreviewPages\productdeletion.png" alt="#"></a>
</p>

 - Register New Staff (admin only view)
<p align="">
 <img width=auto height=auto src="media\PreviewPages\registerstaff.png" alt="#"></a>
</p>

 - Sales Admin View 
<p align="">
 <img width=auto height=auto src="media\PreviewPages\sales.png" alt="#"></a>
</p>

 - Staff Sales View 
<p align="">
 <img width=auto height=auto src="media\PreviewPages\sales(staff).png" alt="#"></a>
</p>

 - Particular Invoice Details
<p align="">
 <img width=auto height=auto src="media\PreviewPages\invoicedetails.png" alt="#"></a>
</p>

 - Deletion of Invoice (admin only) 
<p align="">
 <img width=auto height=auto src="media\PreviewPages\invoicedeletion.png" alt="#"></a>
</p>





