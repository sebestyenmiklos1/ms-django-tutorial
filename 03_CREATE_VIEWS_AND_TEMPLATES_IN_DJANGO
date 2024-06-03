When you're first beginning to create websites, having static pages seems only natural. But what if you want to get a little creative and have data change per user or per page?

That's where using templates can ease the process of developing apps. Templates give you the option to use the same page multiple times throughout the site, with sections of data that can continuously change depending on the request.

This module shows you why creating dynamic pages is worth the time. It also shows you how to easily create and manage them.

In this module, you'll learn how to:

- Work with views.
- Use template variables and tags.
- Add dynamic data to Django templates.
- Use template inheritance.

## Get Started with views

### Create a view

To create a view from scratch in Django, you typically create a function. The function commonly contains the appropriate code to:

Perform the task that the user has requested.
Return a template with the appropriate data to display to the user.
View functions always take at least one parameter named request, which represents the user's request. You can provide more parameters as needed if you're expecting more information from the user in the URL, such as the name or ID of an item. You'll register those when creating the route, which we talk about later in the unit.

### 404 errors

A 404 error in web applications means "not found." As a best practice, you should return a 404 whenever a request is made for an object that doesn't exist.

get_object_or_404 and get_list_or_404: Loads an object by a primary key, or returns a 404 to the user if an object is not found.
get_list_or_404: Performs the same operation as the other shortcut, except that it accepts a filter parameter.

We'll use get_object_or_404 in our exercise.

### Rendering the template

Django's templating engine will take the HTML template that we build, combine it with any data that we provide, and emit the HTML for the browser. The helper function to perform this task is render.

The render function needs the object that represents the request, which is the request parameter that we highlighted earlier. You also pass in the name of the template, typically an HTML file that will reside in a folder named templates.

To pass data into the template, you provide render with a context dictionary object. The context object contains a set of key/value pairs, where each key becomes a variable in the template.

### Example

To create a view to display all shelters, you might use the following code:

```Python
def shelter_list(request):
    shelters = Shelter.objects.all()
    context = { 'shelters': shelters }
    return render(request, 'shelter_list.html', context)
```

### Register a path

Register a path in the urls.py of the app and the urls.py in project folder should include all.

project urls.py:

```Python
from django.contrib import admin
from django.urls import path
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('hello_world.urls')),
    path('', include('dog_shelters.urls'))
]
```

App urls.py:

```Python
from django.urls import path
from . import views

urlpatterns = [
    path('shelters', views.shelter_list, 'shelter_list'),
    path('shelter/<int:pk>', views.shelter_detail, name='shelter_detail')
]
```

Almost any web framework uses paths to process user requests. Paths convert the portion of the URL after the name of the domain and before the query string (which comes after the question mark) into a function call.

We can also create virtual folders for specific requests. For example, if we wanted to list all shelters if someone requests /shelters, we could use the following command:

```Python
path('shelters', views.shelter_list, 'shelter_list')
```

### URL Parameters

It's a common practice to pass parameters to an application as part of the URL, such as an ID or a name. Because these values will change, we don't want to hard code them into our path. In Django, you can specify a parameter by using a special syntax. In that syntax, you can indicate the type of data you're expecting, such as an integer, and a name.

For example, to create a path for someone to request a specific shelter by an ID, we would want a parameter of type integer. (The reason is that our primary key is an integer.) We can then provide the name that we want to use for the variable, which will then be passed in as a parameter to the view function. The syntax for identifying this parameter would be <int:pk>. Notice the type declaration, the colon, and then the name of the variable.

The full path might look like this:

```Python
path('shelter/<int:pk>', views.shelter_detail, name='shelter_detail')
```

The associated view function would have the following signature:

```Python
def shelter_detail(request, pk):
    # code
```

## Exercise - Create views


### Create views

Finish the dog_shelters/views.py:

```Python
from django.shortcuts import render, get_object_or_404
from . import models

# Create your views here.
def shelter_list(request):
    shelters = models.Shelter.objects.all()
    context = { 'shelters': shelters }
    return render(request, 'shelter_list.html', context)

def shelter_detail(request, pk):
    shelter = get_object_or_404(models.Shelter, pk=pk)
    context = {'shelter': shelter}
    return render(request, 'shelter_detail.html', context)
```

### Create the URLconf

```Python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.shelter_list, name='shelter_list'),
    path('shelter/<int:pk>', views.shelter_detail, name='shelter_detail')
]
```

Notice that we created a default path ('') to point to our shelter_list view. We also registered shelter/<int:pk> to reference our shelter_detail view. As highlighted earlier, pk will be passed as the pk parameter to shelter_detail.

## Get started with Django templates

Templates are text files that can be used to generate text-based formats such as HTML or XML. Each template contains some static data that's shared across the site, but it can also contain placeholders for dynamic data. Templates contain variables and tags that control the behavior and what will appear as the final page.

Let's explore how templates work in Django.

### Variable

Variables in a template behave as they do in any other programming language. We can use them to indicate a value that's evaluated at runtime.

Django provides a way to display variables in a template by using the {{ }} syntax. Any variable placed inside the double curly braces is evaluated for its text content and then placed into the template. If we wanted to display the dog's name, for example, we could use {{dog.name}}.

The view passes variables into a template by using the render function, which we'll explore in a later module. You can pass values and other data to a template, including a QuerySet from the Django ORM. This allows you to display data from the database for your application.

### Filters

Filters are a great way to control how the data appears when it's requested in a template. Because filters are already created, they provide an easy way for you to format data without having to write any special code.

For example, let's say we have to print out the names of the dog breeds, and we want to make sure the first letter of every name is capitalized.

```HTML
{{ dog.name | capfirst }}
```

The variable is to the left of the pipe symbol (|), and the filter is on the right. This is just one of many filters that you can use to manipulate the data when you're using Django template filters.

### Tags

You can use tags to perform loops, create text, or provide other types of commands for the template engine. Tags often resemble Python syntax. But because they run inside the template (rather than inside the Python interpreter), you'll notice some slight differences in syntax. Without the ability to rely on tabs like we would with Python, each block statement will require a corresponding end.

We can use if statements for Boolean logic, and for loops for iteration. The core syntax for if statements looks like the following:

```HTML
{% if dogs %}
    <h2>There are {{ dogs | length }} ready for adoption!</h2>
{% else %}
    <h2>We have no dogs ready for adoption. Please check back later!</h2>
{% endif %}
```

Similarly, we can use a for loop to display the names of all dogs in a list:

```HTML
<ul>
    {% for dog in dogs %}
        <li>{{ dog.name }}</li>
    {% endfor %}
<ul>
```

### Template inheritance

Templates are used to generate the HTML that you want the user to see while using your application. Pages in an application typically share a common structure, where navigation might be on the left, a title is on the top, and there's a consistent stylesheet. Django templates support shared structures through inheritance.

#### Create a parent page

Creating a parent page is the same as creating any Django HTML template. You provide the outer structure and then include {% block %} placeholders. These placeholders allow the children to provide the content to be placed in those placeholders.

Let's create a parent page to import a stylesheet, provide a default title, and provide a header that we want to display on all pages:

```HTML
<html>
<head>
    <link rel="stylesheet" href="site.css">
    <title>{% block title %}Shelter site{% endblock %}</title>
</head>
<body>
    <h1>Shelter site</h1>
    {% block content %}
    {% endblock %}
</body>
</html>
```

#### Create a child page

We can create a child page from the parent by using the extends keyword. With this keyword, we provide the name of the HTML file of the parent template. We then use the appropriate {% block %} statements to add the content specific to that page.

```HTML
{% extends "parent.html" %}

{% block title %}
Welcome to the Shelter site!
{% endblock %}

{% block content %}
Thank you for visiting our site!
{% endblock %}
```

When the page is displayed, it looks like the following:

```HTML
<html>
<head>
    <link rel="stylesheet" href="site.css">
    <title>Welcome to the shelter site</title>
</head>
<body>
    <h1>Shelter site</h1>
    Thank you for visiting our site!
</body>
</html>
```

## Exercise - Create templates

Let's create two templates to display a list of shelters, and a detail page for each shelter. We'll also create a base template to ensure consistency across our application.

### Create the base template

1. In Visual Studio Code, create a new folder inside dog_shelters named templates.
1. Create a new file inside templates named base.html.
1. Add the following HTML to base.html:
```HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Dog shelter site{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css" integrity="sha384-B0vP5xmATw1+K9KRQjQERJvTumQW0nPEzvF6L/Z6nronJ3oUOFUFpCjEUQouq2+l" crossorigin="anonymous">
</head>
<body>
    <article class="container">
        <section class="jumbotron">
            <h3>Dog shelter application</h3>
        </section>
        {% block content %}
        {% endblock %}    
    </article>
</body>
</html>
```

Notice the two {% block %} statements, one for the title and the next for the content that the child pages will provide. We're providing a default value for title, which ensures that we'll always have a title if a child page doesn't set it.

### Create the shelter list template

We'll now create another template for listing all shelters. We'll loop through the list of shelters and create links to details for all shelters.

In dog_shelters/templates, create a new file named shelter_list.html.

Add the following code to create the template for our shelter list:

```HTML
{% extends 'base.html' %}

{% block title %}
Shelter list
{% endblock %}

{% block content %}
<h2>Shelter list</h2>
<div>Here is the list of registered shelters</div>
    {% for shelter in shelters %}
        <div>
            <a href="{% url 'shelter_detail' shelter.id %}">
                {{shelter.name}}
            </a>
        </div>
    {% endfor %}
</div>
{% endblock %}
```

We use the block tags to indicate where we want our information to be placed. We specify a title value of Shelter list, and the content items will be the list of all shelters.

We're also using a new tag, url. The url tag generates a URL dynamically. Our URLs are registered in our URLconf, so they can potentially change. By using the url tag, we can tell Django to retrieve the appropriate URL from the URLconf rather than hard-coding in a path.

The url tag looks for the name of the path, shelter_detail in our case, and then the list of any expected parameters. shelter_detail has one parameter, pk. That's the primary key, or ID, of the shelter. We specify the ID by using shelter.id.

### Create the shelter detail template

With our list template created, we can now create the detail template.

In dog_shelters/templates, create a new file called shelter_detail.html.

Add the following code to create the template:

```HTML
{% extends 'base.html' %}

{% block title %}
Shelter list
{% endblock %}

{% block content %}
<h2>{{ shelter.name }}</h2>
<div>Located in {{ shelter.location }}</div>
{% if shelter.dog_set.all %}
    <div>Here is the list of available dogs</div>
    {% for dog in shelter.dog_set.all %}
        <div>
            <a href="">
                {{dog.name}}
            </a>
        </div>
    {% endfor %}
    </div>
{% else %}
    <div>This shelter has no dogs available for adoption</div>
{% endif %}
{% endblock %}
```

Notice that in the body, we check to see if any dogs are inside the shelter by using if shelter.dog_set.all. If there are dogs, we display the list by using for to loop through all the dogs. Otherwise, we display a message that says no dogs are available. We'll update the link in a later unit.

You might notice that we're making two calls to shelter.dog_set.all. If you're experienced with databases and ORMs, you might be concerned that we're making two calls to the database. Two calls would normally be a performance hit. Django has built-in caching, which will ensure that only one call to the database is made.