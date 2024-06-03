When you create applications, you'll eventually want to create individual permissions for site access. Creating an admin interface for employees or clients to manipulate content can be a cumbersome task. Once again Django comes to the rescue with a simple admin feature that's automatically created in projects. We now continue our journey through the Django platform by activating the admin site, adding user permissions, and exploring another view of the database.

In this module, you'll learn how to:

Enable the admin site.
Create a super user.
Add app models and access data.
Set user permissions.

## Permissions for the admin site

Django includes a built-in admin site that can be used to manage the data in your application and security. This site is part of the default installation. As we'll see, it requires only a few lines of code to fully activate it. Django also includes a full authentication and authorization implementation, which you can use to control access to the admin site.

Django is designed to streamline the creation of data-driven web applications by providing the normal functionality that's required by these types of sites. Django provides an authentication and authorization mechanism, and you're free to expand and modify the included system. You can incorporate third-party authenticators, multifactor authentication, or any other requirements your organization might have. We'll explore the default implementation in this module.

Django has three main types of users by default: __users__, __staff__, and __superusers__. You can create your own types by making groups or setting unique permissions.

Access	User	Staff	Superuser
Admin site	No	Yes	Yes
Manage data	No	No	Yes
Manage users	No	No	Yes

## Create User

To create users in Django, you must first create a superuser. Use the command __createsuperuser__ from manage.py to create a superuser. After you create a superuser, you can access the admin site to create any other users.

```BASH
python manage.py createsuperuser
```

Creating a data-driven application means, by definition, working with data. Allowing internal business users access to modify the data as they see fit often requires quite a bit of code between security and the interface. Django provides an admin site that handles this process for you.

Through the admin site, you can determine which users have access to what data. Users can then use the admin site to add, update, and delete items. They don't need to access the database directly or bypass any of the validation rules you've implemented. The security model and interface are already created for you as part of the framework. All you need to do is activate your models so they appear in the site, which requires only a couple of lines of code.

### Sign in to the admin site

http://localhost:8000/admin

## Manage Data

As highlighted before, the admin site doesn't provide access to your data by default. Fortunately, it takes only a couple of lines of code to register any models you want to be editable through the tool.

### Register models

Open dog_shelters/admin.py:

```Python
# Register your models here.
from .models import Shelter, Dog

admin.site.register(Shelter)
admin.site.register(Dog)
```

Save the file. Return to your browser, and refresh the page. Notice that you have Dogs and Shelters listed under DOG_SHELTERS.

## Manage permissions

As highlighted earlier, you can add users with permissions to modify data through the admin site. Let's update the staffuser user we created in a prior unit to have permissions to modify dogs.

Return to the admin site in your browser.

Select Users.

Select staffuser to update our staffuser.

Ensure Staff status is selected.

Scroll down to User permissions.

Select the following permissions:

dog_shelters | dog | Can add dog
dog_shelters | dog | Can change dog
dog_shelters | dog | Can view dog

Sign in as the staff user

We've now configured a staff user with limited permissions in the admin site. You can use this capability to control access to sensitive data in your application.



