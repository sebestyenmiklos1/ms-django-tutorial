## Initial setup

Create and activate virtual environment:

```BASH
# Windows
python -m venv .django-tutorial-env
.\\.django-tutorial-env\\Scripts\\Activate
pip install -r src/requirements.txt

# macOS or Linux
python3 -m venv .django-tutorial-env
source ./.django-tutorial-env/bin/activate
pip install -r src/requirements.txt
```

## Create a project with Django-admin

```BASH
django-admin startproject helloproject . 
```

The trailing period at the end of the command is important. It instructs django-admin to use the current folder. If you leave off the period, it will create an additional subdirectory.

## Run the project

```BASH
python src/manage.py runserver
```

## Create app and register with project

Because apps and projects are separate in Django, you must register your app with the project. This is done by updating the INSTALLED_APPS variable inside __settings.py__ for the project, adding a reference to the config class for the app. The config class is found in apps.py, and is the same name as the project. In our example, the class will be named HelloWorldConfig. E.g:

``` python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hello_world.apps.HelloWorldConfig', # Function name at django-tutorial\hello_world\apps.py
]
```

## Create paths and views

1. open views.py, which will be inside hello_world
1. Replace the code inside views.py with the following code. The helper function HttpResponse allows you to return text or other primitive types to the caller.
```python
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world!")
```
1. create a file in hello_world named urls.py with content
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```
1. Register our URLconf with the project. Our newly created URLconf is inside our hello_world application. Because the project controls all user requests, we need to register our URLconf in the core urls.py file, which is inside helloproject.
    1. Open urls.py inside helloproject
    ```python
    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [
        path('', include('hello_world.urls')),
        path('admin/', admin.site.urls),
    ]
    ```
1. Run your first app: `python manage.py runserver`










