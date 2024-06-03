## Introduction

Although it's possible to create applications that interact with a relational database directly, this direct interaction can lead to code that's duplicated and not secure. This problem led to the introduction of object-relational mappers (ORMs), which separate database calls from objects.

As a developer, you can use ORMs to design objects that represent your data. ORMs can also manage database operations for you.

Django has a built-in ORM, which is a core component of the framework. In this module, we'll explore the Django ORM, how to create model objects, and how to interact with the database through the ORM.

In this module, you'll learn:

- The purpose of an ORM.
- How to set up and activate the Django SQLite database.
- How to create and activate Django models.
- Why the __str__ method is an important addition in classes.
- How to create and query data in your SQLite database.

## Create a model

In Django, a model is any class that inherits a collection of functionality from django.models.Model. The collection includes methods that allow you to query the database, create new entries, and save updates. You can also define fields, set metadata, and establish relationships between models.

If you wanted to create two models, Product and Category, you would add two classes:

```python
from django.db import models
class Product(models.Model):
    # details would go here
    pass

class Category(models.Model):
    # details would go here
    pass
```

## Add fields

The core piece of metadata for all fields is the type of data that it will store, such as a string or a number. Field types map both to a database type and an HTML form control type (such as a text box or a check box). Django includes several field types, including:

CharField: A single line of text.
TextField: Multiple lines of text.
BooleanField: A Boolean true/false option.
DateField: A date.
TimeField: A time.
DateTimeField: A date and time.
URLField: A URL.
IntegerField: An integer.
DecimalField: A fixed-precision decimal number.

To add fields to our Product and Category classes, we might have the following code:

```python
from django.db import models
class Product(models.Model):
    name = models.TextField()
    price = models.DecimalField()
    creation_date = models.DateField()

class Category(models.Model):
    name = models.TextField()
```

You can use field options to add metadata to allow null or blank values, or mark a field as unique. You can also set validation options and provide custom messages for validation errors.

As with field types, field options map to the appropriate settings in the database. The rules will be enforced in any forms that Django generates on your behalf.

Field options are passed into the function for the field itself. Different fields might support different options. Some of the most common are:

A standard practice in relational databases is for each row in a table to have a primary key, typically an automatically incremented integer. Django's ORM will add this key automatically to every model that you create, by adding a field named id.

If you want to override this behavior, you can set the field that you want to be your primary key. However, you should rely on Django's id field in most situations.

Relational databases also have relationships between tables. A product has a category, an employee has a manager, and a car has a manufacturer. Django's ORM supports all the relationships that you might want to create between your models.

The most common relationship is "one-to-many," technically known as a foreign key relationship. In a foreign key relationship, multiple items share a single attribute. Multiple products are grouped into a single category, for example. To model this relationship, you use the ForeignKey field.

To create the relationship, you add the ForeignKey field to the child object. If your products are grouped into categories, you add the category property to the Product class, and you set the type to be ForeignKey.

Django automatically adds a property to the parent to provide access to all children called <child>_set, where <child> is the name of the child object. In our example, Category will automatically have product_set added to provide access to all products in the category.

ForeignKey has one mandatory parameter, on_delete. This parameter tells Django what to do if the parent is deleted. That is, if we delete a category, what should happen to the products in that category?

The two most common options are:

CASCADE, which will delete all products if a category is deleted in our example.
PROTECT, which will return an error if we try to delete a category that contains products.

```python
from django.db import models
class Product(models.Model):
    name = models.TextField()
    price = models.DecimalField()
    creation_date = models.DateField()
    category = models.ForeignKey(
        'Category', #The name of the model
        on_delete=models.PROTECT
    )

class Category(models.Model):
    name = models.TextField()
    # product_set will be automatically created
```

## Create and Register models

Create models in __models.py__ in the app.

E.g.:

```python
# Create your models here
class Shelter(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Dog(models.Model):
    shelter = models.ForeignKey(Shelter, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    description = models.TextField()
    intake_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
```

All applications must be registered with the project in Django. It might seem a little counterintuitive, but just because an application folder exists inside a project doesn't mean it automatically gets loaded. We need to register it by adding it to the INSTALLED_APPS list.

## Manage the database

The Django ORM goes beyond allowing you to interact with data. You can also use it to create and update the database itself through a process known as migrations.

A migration is a collection of updates to be performed on a database's schema. A database schema is the definition of the database itself, including all tables and columns, and relationships between those tables.

Migrations are used to create and update the database as our models change. As you likely know, software is constantly changing. How we define our models today might be different from how we define them tomorrow. Migrations abstract the process of updating the database away from us. We can then make changes to our models and use Django to perform the necessary changes to the database.

### Make a migration

To create a migration, you use the `makemigrations` command in __manage.py__. 

The makemigrations command uses the current list of migrations to get a starting point, and then uses the current state of your models to determine the delta (the changes that need to be made). It then generates the necessary code to update the database. After makemigrations runs, it displays the name of the migration.

```python
python manage.py makemigrations
```

```python
Migrations for 'dog_shelters':
  dog_shelters\migrations\0002_remove_dog_adoption_date_alter_dog_description_and_more.py
    - Remove field adoption_date from dog
    - Alter field description on dog
    - Alter field id on dog
    - Alter field id on shelter
```

### Display the SQL for the migration

Any operations that happen inside a relational database require Structured Query Language (SQL). Django's migrations generate the appropriate SQL when they're run. Although you can use the migration tools to update your database directly, some environments might have database administrators who will manage the process for you.

To build the appropriate SQL statements, you can use sqlmigrate.

```BASH
python manage.py sqlmigrate <app_label> <migration_name>
```

Note: The app_label part is the name of your app, typically the name of the folder that contains your app. The migration_name part is the name of the migration. You can also see the Python code for any app's migrations in its migrations folder.

e.g.: 

```BASH
python manage.py sqlmigrate dog_shelters 0002_remove_dog_adoption_date_alter_dog_description_and_more
```

```SQL
BEGIN;
--
-- Remove field adoption_date from dog
--
ALTER TABLE "dog_shelters_dog" DROP COLUMN "adoption_date";
--
-- Alter field description on dog
--
CREATE TABLE "new__dog_shelters_dog" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "description" text NOT NULL, "name" varchar(200) NOT NULL, "intake_date" datetime NOT NULL, "shelter_id" integer NOT NULL REFERENCES "dog_shelters_shelter" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__dog_shelters_dog" ("id", "name", "intake_date", "shelter_id", "description") SELECT "id", "name", "intake_date", "shelter_id", "description" FROM "dog_shelters_dog";
DROP TABLE "dog_shelters_dog";
ALTER TABLE "new__dog_shelters_dog" RENAME TO "dog_shelters_dog";
CREATE INDEX "dog_shelters_dog_shelter_id_bf695502" ON "dog_shelters_dog" ("shelter_id");
--
-- Alter field id on dog
--
CREATE TABLE "new__dog_shelters_dog" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "description" text NOT NULL, "intake_date" datetime NOT NULL, "shelter_id" integer NOT NULL REFERENCES "dog_shelters_shelter" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__dog_shelters_dog" ("name", "description", "intake_date", "shelter_id", "id") SELECT "name", "description", "intake_date", "shelter_id", "id" FROM "dog_shelters_dog";
DROP TABLE "dog_shelters_dog";
ALTER TABLE "new__dog_shelters_dog" RENAME TO "dog_shelters_dog";
CREATE INDEX "dog_shelters_dog_shelter_id_bf695502" ON "dog_shelters_dog" ("shelter_id");
--
--
--
CREATE TABLE "new__dog_shelters_shelter" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "location" varchar(200) NOT NULL);
INSERT INTO "new__dog_shelters_shelter" ("name", "location", "id") SELECT "name", "location", "id" FROM "dog_shelters_shelter";
DROP TABLE "dog_shelters_shelter";
ALTER TABLE "new__dog_shelters_shelter" RENAME TO "dog_shelters_shelter";
COMMIT;
```

### Display the list of migrations

If you want to see all migrations, you can use showmigrations.

```BASH
python manage.py showmigrations
```

```BASH
admin
 [ ] 0001_initial
 [ ] 0002_logentry_remove_auto_add
 [ ] 0003_logentry_add_action_flag_choices
auth
 [ ] 0001_initial
 [ ] 0002_alter_permission_name_max_length
 [ ] 0003_alter_user_email_max_length
 [ ] 0004_alter_user_username_opts
 [ ] 0005_alter_user_last_login_null
 [ ] 0006_require_contenttypes_0002
 [ ] 0007_alter_validators_add_error_messages
 [ ] 0008_alter_user_username_max_length
 [ ] 0009_alter_user_last_name_max_length
 [ ] 0010_alter_group_name_max_length
 [ ] 0011_update_proxy_permissions
 [ ] 0012_alter_user_first_name_max_length
contenttypes
 [ ] 0001_initial
 [ ] 0002_remove_content_type_name
dog_shelters
 [ ] 0001_initial
 [ ] 0002_remove_dog_adoption_date_alter_dog_description_and_more
hello_world
 (no migrations)
sessions
 [ ] 0001_initial
```

### Perform a migration

The migrate command runs a specific migration or all migrations on the database configured in settings.py in the root of your project folder.

If you open settings.py, you'll see a DATABASES section at the bottom. This section includes a default option, which on a new project is configured to use SQLite. You can configure different database connection strings in this section as needed.

```BASH
python manage.py migrate <app_label> <migration_name>
```

NOTE: The app_label and migration_name parts are optional. If you don't provide either, all migrations will run. You'll use this command often during development. Without specifying the app label and the migration name, all the migration is executed.

```BASH
python manage.py migrate
```

```BASH
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying dog_shelters.0001_initial... OK
  Applying dog_shelters.0002_remove_dog_adoption_date_alter_dog_description_and_more... OK
  Applying sessions.0001_initial... OK
```

## Work with data

### Configure the interactive shell

Django includes an interactive shell where you can run Python code in the Django environment.

1. Return to the terminal in Visual Studio Code by selecting View > Terminal.
1. Enter the following command to start the shell:
```Bash
python manage.py shell
```
1. Import the models from models inside dog_shelters:
```Python
from dog_shelters.models import Shelter, Dog
```

### Create and modify objects

Create a new shelter:

```Python
shelter = Shelter(name="Demo shelter", location="Seattle, WA")
shelter.save()
```

Update the shelter:

```Python
shelter.location = "Redmond, WA"
shelter.save()
```

Create two new dogs for the shelter by running the following Python commands in the shell:

```Python
Dog(name="Sammy", description="Cute black and white dog", shelter=shelter).save()
Dog(name="Roscoe", description="Lab mix", shelter=shelter).save()
```

As before, save inserts the dog. Notice how we set the shelter parameter to the shelter object that we created before. Django will automatically set the relationship in the database.

Also note that we didn't set up a local variable for each Dog instance. Because we won't reuse the objects, we don't need to set them to a variable.

### Retrieving objects

To retrieve objects from a database, Django provides an objects property on all Model classes. The objects property provides multiple functions, including all, filter, and get.

Retrieve all dogs in Demo shelter by running the following command:

```Python
shelter.dog_set.all()
```

```BASH
<QuerySet [<Dog: Sammy>, <Dog: Roscoe>]>
```

Retrieve the second dog by using get as shown in the following command:

```Python
Dog.objects.get(pk=1)
```

The get function will return only one object. You can pass parameters into get to provide a query string. Here we use pk, which is a special keyword to indicate the primary key. The returned result will be Sammy.

```BASH
<Dog: Sammy>
```

Retrieve all dogs in Demo shelter by using filter as shown in the following command:

```Python
Dog.objects.filter(shelter__name='Demo shelter')
```

Like get, filter allows us to pass a query in the parameters. Notice we can use two underscores (__) to go from property to property. Because we want to find all dogs in the shelter named Demo shelter, we use shelter__name to access the name property of shelter. The result returned will be all dogs, because we have only one shelter

```BASH
<QuerySet [<Dog: Sammy>, <Dog: Roscoe>]>
```

### Close the shell

```Python
exit()
```
