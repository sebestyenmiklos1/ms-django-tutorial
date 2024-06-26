In this module, you'll walk through the steps to prepare a Django application for production. You'll then create a database and hosting environment for your application by using Visual Studio Code.

You'll finish by deploying your site to Azure and seeing your application run in the cloud.

In this module, you'll learn how to:

- Configure an application for production.
- Install an extension in Visual Studio Code.
- Use the Azure Databases extension to create a PostgreSQL database.
- Use the App Service extension to deploy a website to Azure.
- Run migrations on a database hosted in Azure.

Deployment considerations

An application running in a production environment has a different set of needs and requirements than it does in a development environment. In particular, security and performance concerns aren't as critical during development as they are in production. So you need to ensure your website is properly configured before deployment.

Django provides a full checklist of predeployment configuration updates. The following sections describe a few common changes you'll want to make before you deploy your app to production.

Debug mode:

As a developer, you want to see any error messages your application might generate. But this information can provide an attacker with insights into how your application runs, potentially allowing unauthorized access. So in settings.py, set the DEBUG option to False before you deploy your app to production.

Secret key:

To protect sensitive information, Django uses a secret key to sign any values that must not be tampered with. During development, the secret key is stored in cleartext in settings.py. When you deploy to production, the secret key should be read from a more secure location, such as Azure App Settings or Azure Key Vault.

Allowed hosts:

The settings.py file contains a list of server names called ALLOWED_HOSTS. This list determines where your application can run from. By default, the empty list allows the app to run from localhost. Update this setting before you deploy to your production host.

## Prepare your application for deployment

### Add libraries

You'll use two new libraries for your project:

whitenoise to serve static files
psycopg2-binary to connect to PostgreSQL, the production database

### Create a production settings file

The values you assign to two core settings, ALLOWED_HOSTS and DATABASES, depend on the environment that hosts the application. The default settings are designed for development. To run your app in production, ensure these settings are updated properly.

ALLOWED_HOSTS controls the servers that are allowed to host or run your application. You'll configure it to allow the site to run from Azure and locally. DATABASES contains the list of available connection strings.

A common way to configure the settings is to create a second Python file that contains the collection of settings for production. Then a check at the end of the settings.py determines whether to use the production settings.

Now you'll create a production settings file and add the check to determine if your application is running in production:

1. Create a new file inside project. Name it azure.py.
1. Add the following code to import os.
```Python
from .settings import *
import os
```
1. Add the following code to the end of the file to override ALLOWED_HOSTS to allow Azure to host the application and to define trusted origins.

```Python
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
```
NOTE: Azure App Service automatically creates an environmental variable named WEBSITE_HOSTNAME. This variable contains the URL for your website. You can use this variable to determine whether your application is running on Azure.
1. Add the following code to configure the database connection string for PostgreSQL.
```Python
hostname = os.environ['DBHOST']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'HOST': hostname + ".postgres.database.azure.com",
        'USER': os.environ['DBUSER'],
        'PASSWORD': os.environ['DBPASS'] 
    }
}
```
NOTE: You'll set the environmental variables on Azure in a later step.
The database connection is for PostgreSQL Flexible Server. For PostgreSQL Single Server, set the USER value to os.environ['DBUSER'] + "@" + hostname.

The connection string you're using is for PostgreSQL. You provide the following information:

- ENGINE: Database type
- NAME: Name of the database
- HOST: URL for the server
- USER: Username to use to connect to the database
- PASSWORD: Password for the user

Add the following code to the bottom of the file to enable whitenoise, which will serve static files.

```Python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Enables whitenoise for serving static files
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

WhiteNoise is middleware that reads user requests for static files such as CSS or JavaScript. It also ensures the files are served correctly. You registered the middleware by updating the MIDDLEWARE array. You registered a STATIC_ROOT to store static files.

Set the SECRET_KEY with one read from environmental variables by adding the following code.

```Python
SECRET_KEY = os.getenv('SECRET_KEY')
```

You'll create a new secret key after you deploy the application and store it as an application setting.

Disable debugging mode by adding the following code.

```Python
DEBUG = False
```

Now that you've created the production settings file, you can update your application to load the file in production. Start by looking for the WEBSITE_HOSTNAME environmental variable. This variable indicates the application is running on Azure.

1. Open settings.py.
1. Add the following code to the end of the file to override the necessary settings when the app runs in production.
```Python
import os
if 'WEBSITE_HOSTNAME' in os.environ: # Running on Azure
    from .azure import *
```
1. Save all files by selecting File > Save all.

You've now configured a Django application for production.

## Deployment Consideration

When you deploy an application to production in the cloud, you have a few considerations. You need to determine how to deploy the application and what database to use. You also need to ensure the production environment is ready.

### Deployment options

You can deploy to Azure in several ways. One of the most convenient ways is to use one of these extensions for Visual Studio Code:

- [Azure Databases](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-cosmosdb)
- [Azure App Service](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azureappservice)

Azure Databases allows you to create the database server and database. Azure App Service allows you to create, configure, and deploy to the web host.

### database consideration

Django is designed for data-driven web applications. So every Django project usually includes a database. During development, you typically use SQLite, which is a file-based database engine.

SQLite is a perfect solution for development because it requires no special installation or services. But the requirements for production typically include scaling, performance, and reliability. SQLite isn't designed to manage these production requirements.

Django natively supports many databases, including MySQL, PostgreSQL, and MariaDB. You can also find providers to enable support for SQL Server, MongoDB, and many other databases.

When you created the production settings file, you configured the environment for PostgreSQL. PostgreSQL is one of the most popular databases for Django. It's also supported by Azure.

### Create the database schema

Django manages the database schema through migrations. Django can generate the SQL to create, or it can update the schema. Or you can use the makemigrations command to make Django update the database directly.

To run migrations on the database, you can secure-shell (or SSH) into App Service. This method allows you to run commands on the web host the way you run them locally.

## Deploy to Azure

This exercise requires a sandbox. A sandbox gives you access to free resources. Your personal subscription won't be charged.

You can use the sandbox only to complete training on Microsoft Learn. Using the sandbox for any other reason is prohibited and may result in permanent loss of access to the sandbox.

To make your site available to the public, you'll deploy it to Azure. You'll use the Azure App Service extension in Visual Studio Code to streamline the process.

### Install the Azure App Service extension

Start by installing the Azure App Service extension in Visual Studio Code:

1. In Visual Studio Code, select the Extensions icon.
1. Screenshot showing the Extensions icon.
1. In the Search Extensions field, type App Service.
1. Under Azure App Service, select Install.

If you already have the [Azure App Service extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azureappservice), make sure it's updated to the latest version. See the last updated date on the extension page. If you're working with the latest version, you should see a RESOURCES node with an App Services node.

### Deploy the application

When you followed the steps to clone the starter repository, you should have also changed directory to the starter folder before opening VS Code. The starter directory contains the manage.py file that signals to App Service that you're deploying a Django web app.

1.In Visual Studio Code, on the toolbar, select the Azure icon.
1.Screenshot showing the Azure icon.
1.Select Sign in to sign in to Azure by using the same account you used to create the sandbox.
1.On the RESOURCES bar of the Azure extension, hover, and select the + (plus sign) icon to create a resource.
1.Screenshot showing the App Service bar. The Deploy icon is highlighted.
1.If prompted to choose a subscription, choose your Azure subscription.
1.Select Create App Service Web App....
1.Screenshot showing how to create a new web app.
1.Provide a unique name for your application.
1.Screenshot showing where to provide an app name.
1.Select Python 3.9 as the runtime stack.
1.Screenshot showing the runtime stack selection.
1.Select a pricing tier.
1.Screenshot showing the the pricing tier selection.
1.The extension creates your web application. The process will take a few moments.
1.When the web app is created, you're asked to deploy the web app to the App Service, select Deploy.
1.Screenshot showing the deployment configuration option.

If you miss the notification to deploy the app or you close the notification, you can also deploy by finding the App Service you created, right-click it, and select Deploy to Web App.

## Create the database server

Now create the PostgreSQL database.

1. Install Azure Databases extensions in VSCode
1. On the RESOURCES bar of the Azure extension, hover, and select the + (plus sign) icon to create a resource.
1. Screenshot of the Databases extension, showing the Create Server icon.
1. If prompted to choose a subscription, choose your Azure subscription.
1. Select Create Database Server....
1. Screenshot showing how to create a new database server.
1. For the Azure Database Server, select PostgreSQL Flexible Server.
1. Screenshot showing a list of available database servers.
1. Enter a unique name for your database server.
1. Important: Make a note of the name you use for your database server.
1. Select the Postgres SKU and options.
1. For the name of the admin user, enter shelter_admin.
1. Enter a secure password, such as "86i^z5#emSk6wu3t10nC*".
1. Important: When you create the password, don't use a dollar sign ($). This symbol can cause issues for connections from Python. Make a note of the password you use.
1. Enter the password a second time to confirm it.
1. For the resource group, select the same resource group that your web app was created in.
1. To find the resource group name and location used to create the web app, find the App Service in the Azure extension, right-click the name, and select View Properties. In the "id" key the resource group name is the part following "/resourceGroups/". The "location" key shows the location. You can also right-click the name of the App Service and select Open in Portal to find the resource group name and location.
1. For the location for new resources, select the same location of the resource group and web app. Important: When you create multiple Azure resources that will communicate with one another, always place them in the same region. This collocation ensures the best performance.

Your server will now be created! This process will take a few minutes.

## Create a database firewall rule to allow access from your dev environment

After the database is created, you need to create a firewall rule to allow your developer environment to access the database. Wait until the database exists before following the next steps to create the rule.

1. Open the Visual Studio Code command palette with F1 or the key combination Ctrl + Shift + P.
1. Search for "PostgreSQL: Configure Firewall" and select it.
1. Screenshot: showing the firewall rule field. "Skip for now" is highlighted.
1. When prompted for the resource to apply the firewall to, select the Postgres database you created.
1. A final dialog box asks to continue and shows the IP address it will add. Select Yes.

It takes a few minutes to add the rule. Watch the VS Code notification window for status.

## Create a database on the database server

Now that you've configured App Service and created the server, you can create the database in the Postgres Database Server.

1. In the RESOURCES of the Azure Tools extension, expand the PostgreSQL Servers (Flexible) node and find the server you created.
1. Right-click the name of your database server and select Create Database.
1. Select the Networking resource of the Postgres Server.
2. Select Allow public access from any Azure service within Azure to this server option in the portal from the Networking tab and select Save.

## Configure application settings for the web app

App Service uses the application settings to configure environmental variables. Settings are a convenient way to store information you shouldn't put in your code, such as database connection strings.

1. Under App Service, expand the sandbox subscription. Then expand your application.
1. To create the first application setting, right-click Application Settings and then select Add New Setting.
1. Screenshot showing how to add a new setting.
1. In the first field, enter the name DBUSER.
1. In the second field, enter the value shelter_admin.
1. Repeat the preceding steps to create the remaining settings:

| Name | Value |
| --- | --- |
| DBHOST | The server name you created previously |
| DBPASS | The password you created previously |
| DBUSER | shelter_admin |
| DBNAME | shelters |
| SECRET_KEY | Generate a secure password |

NOTE:

## Create the schema and superuser

The last step in the deployment is to set up the database. In local development, you run python manage.py migrate and python manage.py createsuperuser to create the database schema and superuser. On Azure, you'll do the same.

You'll connect to the web server in Azure by using Secure Shell (SSH). You can make the connection in Visual Studio Code as shown below.

1. In the App Service extension, right-click your app service and then select SSH into Web App.
2. An SSH connection will be made to your web server in Azure. This process might take a few minutes. A terminal pane appears in Visual Studio Code. This terminal is the SSH connection to your web server. If you have trouble connecting, [see the troubleshooting steps](https://learn.microsoft.com/en-us/training/modules/django-deployment/6-deploy-azure#troubleshooting-ssh) below.
3. 

