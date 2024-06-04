## Introduction

Data-driven applications often share a similar structure. You have a page where you list items, a page to display the details of an item, and then the appropriate pages to allow creation, updates, and deletes. Having to create each of these pages by hand can become tedious, especially since much of the code and HTML is repetitive.

To help streamline the creation of data-driven applications, Django provides generic views. Generic views are class-based views designed to perform all of these common operations. We can use generic views to quickly create pages to display and edit data. These views can even generate the HTML forms for us!

In this module, we'll explore generic views and forms, and how we can use a common library to enhance the display of our forms.

In this module, you'll learn how to:

Use generic views.
Create Django forms.
Use the django-crispy-forms library.

## Use generic views to display data

The generic views system in Django streamlines the creation of repetitive code. The common operations you perform in a data-driven application share the same pattern. For example, to display an individual item by its ID or primary key, the workflow is always:

Load the item from the database by ID.
If the item isn't found, return a 404.
If the item is found, pass the item to a template for display.
The generic view system acknowledges this fact and provides classes you can use that contain the core code already written. You inherit from the appropriate class, set a couple of properties, and then register an appropriate path in your URLconf. The rest is taken care of for you!

Django includes two generic views for displaying data: DetailView and ListView.

### DetailView for item detail

The generic view DetailView is used to display a detail page for an item. DetailView retrieves the item for the specified model by the primary key and passes it to the template. You can set template_name to the name of the template to be used. The default is <model>_detail.html. Finally, we can set context_object_name to the name of the variable we want to use in our template.

To create a detail view by using the generic view for a dog, you could use the following code:

```Python
from . import models
from django.views import generic

class DogDetailView(generic.DetailView):
    model = models.Dog
    template_name = 'dog_detail.html'
    context_object_name = 'dog'
```

Registering DogDetailView is similar to any other path entry. The key thing to ensure you include is a parameter named pk. Django uses this convention to identify the primary key. You'll also note we use the as_view() method to convert the class into a view.

```Python
path('dog/<int:pk>', views.DogDetailView.as_view(), name='dog_detail')
```

### ListView for a list of items

The generic view ListView behaves in a similar fashion to DetailView. You can set context_object_name for the name of the variable in the view and template_name for the name of the template.

The primary difference is that ListView is designed to work with any form of a query that returns multiple items. As a result, you must override the get_queryset function. The functionget_queryset is called by the generic view system to retrieve the items from the database, which allows you to order or filter your items as needed.

To create a view to display the list of all shelters by using the generic view ListView, you could use the following code:

```Python
from . import models
from django.views import generic

class ShelterListView(generic.ListView):
    template_name = 'shelter_list.html'
    context_object_name = 'shelters'

    def get_queryset(self):
        return models.Shelter.objects.all()
```

Registering the view is performed much in the same way as our DetailView.

```Python
path('', views.ShelterListView.as_view(), name='shelter_list')
```

## Exercise - Implement generic views to display data


### Create the HTML template

Now you'll create the HTML template to display out the details of the dog. The object name will be dog as we set that when creating the form.

1. Inside Visual Studio Code, create a new file inside dog_shelters/templates named dog_detail.html.
1. Add the following code to dog_detail.html to create the template to display the details for the dog.
```HTML
{% extends 'base.html' %}

{% block title %}
{{ dog.name }}
{% endblock %}

{% block content %}
<h2>{{ dog.name }}</h2>
<div>About {{ dog.name }} - {{ dog.description }}</div>
{% endblock %}
```

### Update the shelter detail page to include our link

With our path registered and template created, we can update the shelter detail template to include links to our dog detail page.

1. Open dog_shelters/templates/shelter_detail.html.
1. Underneath the line that reads {# TODO: Add link to dogs #}, add the following code to create a link for each dog to the detail view.
```HTML
{# TODO: Add link to dogs #}
<a href="{% url 'dog_detail' dog.id %}">
    {{dog.name}}
</a>
```

## Use generic views to edit data

Like the code required to display data, the code to allow users to modify data is repetitive. It can also be tedious because several steps are required to ensure the data is valid and sent correctly. Fortunately, the generic view system can streamline the amount of code we need to enable this functionality.

### Create new items

Before we explore how Django can streamline our development, we should review the process that allows users to modify data. Let's explore the workflow the server uses to manage the process of creating a new item or piece of data, and the work that goes into creating the HTML form.

#### Creation workflow

At the surface, the code to allow a user to create an item might seem trivial. As it turns out, it's a deceptively involved process.

1. The user sends a GET request to signal they want the form to create a new item.
1. The server sends the form with a special token to prevent cross-site request forgery (CSRF).
1. The user completes the form and selects submit, which sends a POST request to 1. indicate the form has been completed.
1. The server validates the CSRF token to ensure no tampering has taken place.
1. The server validates all information to ensure it meets the rules. An error message is returned if validation fails.
1. The server attempts to save the item to the database. If it fails, an error message is returned to the user.
1. After successfully saving the new item, the server redirects the user to a success page.

This process requires quite a bit code! Most of it's boilerplate, which means it's the same every time you create it.

#### Forms

Creating an HTML form can be a tedious process. Developers are often copying and pasting input tags, looping through lists to create drop-downs lists, and setting up radio buttons. Whenever the model changes, the form must be updated.

You might have noticed the models we create in Django contain everything necessary to create the form. When we added the various fields, we indicated the data types, which are coupled with different HTML elements. For example, a Boolean field would be a check box and a foreign key would commonly be a drop-down list.

### Generic views to modify data

One of Django's key goals is to eliminate the need to constantly re-create the same blocks of code over and over. To support this goal for data modifications, Django provides a collection of generic classes and forms to manage this workload for us. As we'll see, it includes all the necessary code and can even create the form for us dynamically. The classes used for creating, updating, and deleting data are called CreateView, UpdateView, and DeleteView.

#### CreateView

The class CreateView is used to allow a user to create items. It walks through the preceding process and dynamically creates the form. After success, it displays the detail page for the newly created item.

You specify the model and template_name you want to associate with it just as you would with the other generic views. The key difference for CreateView is the inclusion of a fields property where you list the editable fields. By using this property, you can ensure fields that shouldn't be edited, like a creation date, don't appear on the form. The view to create a new dog might look like the following sample:

```Python
from . import models
from django.views import generic

class DogCreateView(generic.CreateView):
    model = models.Dog
    template_name = 'dog_form.html'
    fields = ['name', 'description', 'shelter']
```

#### UpdateView

The class UpdateView behaves in an identical fashion to CreateView. The only difference is that it automatically loads an item based on the pk parameter. Django uses this convention for the primary key for an item.

```Python
from . import models
from django.views import generic

class DogUpdateView(generic.CreateView):
    model = models.Dog
    template_name = 'dog_form.html'
    fields = ['name', 'description', 'shelter']
```

After successfully creating or updating an item, Django redirects to the details page for the item. It retrieves the URL for the details by using get_absolute_url on the associated model. You implement this method by returning the correct URL. You can retrieve the appropriate URL from URLconf by using reverse. Note kwargs is used to pass the pk or primary key parameter to the route.

```Python
from django.db import models
# TODO: Import reverse
from django.urls import reverse
class Dog(models.Model):
    # Existing code
    def get_absolute_url(self):
        return reverse('dog_detail', kwargs={"pk": self.pk})
```

#### DeleteView

The class DeleteView is similar to UpdateView. It allows a user to delete an item and identifies the item to be deleted by using pk. Unlike UpdateView, fields isn't needed because you'll be deleting the entire item. Also, because no item has been newly created or updated, we need to determine where we want to redirect the user. We can create a redirect by setting the success_url to the appropriate value. You can look up a URL by using reverse_lazy.

```Python
from . import models
from django.views import generic
from django.urls import reverse_lazy

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')
```

## Form templates for create and update

The generic views can create the HTML form for us dynamically. All we need to provide is a template to act as the placeholder for the form. The placeholder template ensures the form matches the rest of our site. Fortunately, we don't need much code to create it.

The generic views automatically create a form variable for our template to use. The form elements provided by Django can be displayed inside <p> tags or as a <table>.

The form variable contains all of the appropriate HTML to create the controls from the form. It doesn't contain the <form> tag itself or a submit button. Our template must include four items:

- The form element with the method set to POST because this setting triggers the save operation on the server.
- The code {% csrf_token %} to add the CSRF token to prevent spoofing.
- The code {{ form.as_p }} or {{ form.as_table }} to display the dynamically generated form.
- The submit button.

The following code can act as the host for any generic view form.

```HTML
<form method="post">{% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>
```

templates/dog_form for example

## Exercise - Implement django-crispy-forms

After you view the created form, you might notice that the formatting isn't the same as the rest of our page. We're using Bootstrap, and the form currently isn't. Fortunately, there's a library that can ensure our forms use Bootstrap too.

The ˙[django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/) library further enhances how forms are generated by Django. We're going to explore how we can use the library to ensure our forms use Bootstrap.

The library has to be installed. `django-crispy-forms` and `crispy-bootstrap4`

django-crispy-forms has to be rgistered in project's settings.py INSTALLED_APPS as `crispy_forms` and `crispy_bootstrap4`. The CRISPY_TEMPLATE_PACK = 'bootstrap4'has to be added to the settings.py too.

### Update our template to use django-crispy-forms

The bulk of the amazing work that django-crispy-forms does is by using a filter. A filter allows you to take a variable in a template and pass it into another handler or process. In our case, the crispy filter will convert our form to the specified template, Bootstrap 4.

Inside Visual Studio Code, open dog_shelters/templates/dog_form.html.

Underneath the line that reads {# TODO: Load crispy_forms_tags #}, add the following code to load the filter or tag.

```Python
{# TODO: Load crispy_forms_tags #}
{% load crispy_forms_tags %}
```
Replace the line that reads {{ form.as_p }} with the following code to use the crispy filter.

```Python
{{ form | crispy }}
```

