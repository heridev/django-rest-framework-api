# Django with the REST framework practice

It was inspired by this [youtube vide](https://www.youtube.com/watch?v=cJveiktaOSQ)
and expanded with additional analysis and study on some specific items

## How to run the server and see the two endpoints(POST and GET)
```
python manage.py runserver
```

## How it was created this functionality?
First of all we started installing the `django` package
```
pip django
```

Scaffolding the project with django
```
django-admin startproject djangorestapi
```

### Explanation about the command
- django-admin: This is Django's command-line utility for administrative tasks. In some cases, depending on how Django is installed and your environment, you might use django-admin.py instead.
- startproject: This is a command provided by django-admin to create a new Django project. A Django project is the entire application with all its parts. It's the top-level container for your web application.
- djangorestapi: This is the name of the new project you're creating. After running this command, Django will create a directory called `djangorestapi` in your current directory.

### What happens when you run this command?

A new Django project directory djangorestapi is created. Inside this directory, several files are created:
- manage.py: A command-line utility that lets you interact with this Django project in various ways.
- A subdirectory (also named djangorestapi by default) containing settings for your project (settings.py), a file for URL declarations (urls.py), and an application configuration file (wsgi.py for WSGI deployment).
This is the first step you would typically take when starting a new Django project.

Next thing is to install the djangorestrframework:
```
pip install djangorestframework
```

And include it in your project in your settings installed_apps:
```
rest_framework
```

There are different ways to configure the rest framework but one way is to separate the rest of your apis from other applications installed, and for that reason we are creating a separate `api` folder and initialize with a file `__init__.py` in it

Also we are creating some views so we can place them in a file called
> views.py
```python
# And this one will have a content like this
from rest_framework.response import Response
from rest_framework.decorators import api_view

# we are using this @api_view decorator for the views and type of request
@api_view(['GET'])
def getData(request):
  person = {'name': 'Dennis', 'address': 'address goes here'}
  return Response(person)
```

And now it is the moment to actually define the URL for our endpoint, so let's create a new file called urls.py with the following content:
```python
from django.urls import path
from . import views

urlpatterns = [
  path('', views.getData),
] 
```

and we would need to conect the api urls we just created and make it accesible to the entire django application
> djangorestapi/urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls'))
]
```

now we can try to see our newly created endpoint by running the server 
```
python manage.py runserver
```

At this point you will see a great interface to manage your JSON api and to make some request and kind of a documentation for everything, which is awesome.

so let's keep going and now let's work a bit with an actual seralization of data and a database(by default sqlite).

Let's separate our logic into a different folder so we get access to that from apis or admin or the web application itself, and for that we can create the core or base folder
```
python manage.py startapp base
```

### Explanation about the commands we just run
- manage.py: This is a command-line utility automatically generated when you create a new - Django project (in your case, djangorestapi). It offers various commands and allows you to manage your Django project.
- startapp: This is a command provided by manage.py that creates a new Django application. A Django application is a web application that does something – e.g., a blog, a database, an API.
- base: This is the name of the new application you're creating. It's a conventional name but can be any valid Python identifier.

### What happens when you run this command?
A new Django app directory base is created within your project.
Inside this directory, Django creates a number of files necessary for the app to function, including:
- models.py: For your database models.
- views.py: For your application's views.
- tests.py: For your app's tests.
- apps.py: For the application's configuration.
- migrations/: A directory for database migration files.

This command sets up a new app within your project, which is a component of your overall Django project. A single Django project can contain multiple apps, each serving a different functionality within the project.

Let's continue and register the new app in the project `settings.py`
```python
INSTALLED_APPS = [
     ....,
    'rest_framework',
    'base',
]
```

And let's add a model example, in the 
> base/models.py

```python
from django.db import models

class Item(models.Model):
   name = models.CharField(max_length=200)
   created = models.DateTimeField(auto_now_add=True)
```

and let's run the migrations
```
python manage.py makemigrations
```

and execute them after they are generated
```
python manage.py migrate
```

If you want to run the console/shell interactive command 
```
python manage.py shell
```

And you can run queries and commands like this:
```python
from base.models import Item
Item.objects.create(name="item # 1")
Item.objects.create(name="item # 2")
Item.objects.create(name="item # 3")
```

And then we can query and see if they were created successfully
```shell
items = Item.objects.all()
print(items)
```

And if all good we can exit the shell
```shell
exit()
```

## Serializers
Serializers in Django and the context of Django REST framework, are a crucial
component for building API services. They are responsible for transforming complex
data types, like Django QuerySets or model instances, into native Python data types
that can then be easily rendered into JSON, XML or other content types.
Serializers also provide deserialization, allowing parsed data to be converted back
into complex types, after validating the incoming data.

### Creating and updating instances
When used for deserialization, serializers can also handle creating and updating model instances. This means they can parse data, validate it and then directly create or update a model instance in the database.

Example
```python
from rest_framework import serializers
from myapp.models import MyModel

class MYmodelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ['id', 'field1', 'field2']
```

So by using that Django REST framework makes it easier to work with HTTP requests and responses, converting and validating JSON/XML content to and from Django models seamlessly. This significantly simplifies the process of building APIs

Let's apply it to our needs.

let's create a file to place some serializers
> api/serializers.py
```python
from rest_framework import serializers
from base.models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
       model = Item
       fields = '__all__'
       # of
       # fields = ['name', 'created_at']
```
In this example we are serializing everything here.

Let's jump into the views that we are declaring our endpoints and data in order to use our new serializer and serialize the data for the collection

> api/views.py
```python
from base.models import Item
# see how we specify the name of the file
from .serializers import ItemSerializer

@api_view(...)
def get_data(request):
    items = Item.objects.all()
    serialized = ItemSerializer(items, many=True)
    return Response(serialized.data)
```

## Undoing migrations by mistake
There are different ways to undo migrations if you made a mistake, but it would depend on the kind of rollback you want to make, as in Django it is very manual the process, you might need to define
- If this is already deployed in a server, you would need to create a new migration to make changes on the current values
- If you havent't run and deploy new migrations created with `makemigrations` in that case, you can just locate the migration and delete it and begin again with the `makemigrations` and then `migrate` changes
- If you already run and migrated your changes you can delete your last migration by specifying one previous migration so the latest will be discarded and will look in the form of
- `0003_xxx` (this is the one you want to delete)
- `0002_xxx` (this is the one you want to make the latest)

so the code might look like this:
```shell
python manage.py migrate your_app_name 0002_xxxx
```

Then delete or modify this migration `0003_xx`

After making changes you can follow the same
- python manage.py makemigrations
- python manage.py migrate

And you would be ready to go

If this is your first migration you might need to use the zero
```shell
python manage.py migrate your_app_name zero
```

### Additional lesson: debug your models attributes
Once in a while you might need to see what are the attributes in a specific model and for that, you can just use
- dir - print(vars(Item.objects.first())) # this one will print a lot of methods, attributes
- vars - print(vars(Item.objects.first())) # this one only shows the kind of database attrs
- or accessing the metadata in the main model
```
Item._meta.get_fields()
```

## Creating a new item
For this we will add a new create_item method in the views similar to get_data

> api/views.py
```python
@api_view(['POST'])
def add_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
```

And lastly we would need to add the route

> api/urls.py
```python
urlpatterns = [
   ...
   path('add/', views.add_item)  
```

after that we would be able to access the browser in that route and make a POST request
> http://localhost:8000/add

with some content like this:
```
{ "name": 'my supper dupper item # 1' }
```

And click the POST request, so we see the response and it should be in the all items 
> http://localhost:8000

There you go, here is the repository with all this content and changes.

