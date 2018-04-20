# Project Layout

Before reading this section, it's recommended to read the [getting started tutorials](https://docs.djangoproject.com/en/2.0/intro/tutorial01/) for Django and to review the [Django documentation](https://docs.djangoproject.com/en/2.0/intro/overview/)


## Directory Structure

	db.sqlite3
	manage.py 
	Procfile 
	requirements.txt 
	runtime.txt 
	mapserver/ 
		templates/ 
			search.html 
		admin.py
		apps.py
		filters.py
		forms.py
		local_settings.py
		models.py
		tests.py
		urls.py
		views.py
	mapserverproj/
		urls.py
		settings.py
		wsgi.py
		...


##Main directory

In the main directory you'll find a few files related to Heroku deployment:

	Procfile
	requirements.txt
	runtime.txt

Your local copy of the database:

	db.sqlite3
	
And your manage.py script which will be used to launch the server and run other commands like migrations
		
## mapserverproj/

This is the parent project for your mapserver app. Very little logic for the mapserver app itself is stored here with some exceptions.

**urls.py**

This is the initial controller logic for the webserver. When a client connects to the server, this file is the first location the server will look to try to find a URL match.

Except for the admin panel, by default all requests will be routed to the urls.py located under the mapserver/ folder

	urlpatterns = [
		path('admin/', admin.site.urls),
		path('',include('mapserver.urls')) #Send all other requests to mapserver.urls file
	]
	
**settings.py**

Your server settings are stored here. It's recommended to check out the Django documentation for specifics.

**wsgi.py**

This file is used for deployment.

## mapserver/

Most of the app specific code is stored here. Things to note:

**admin.py** 

Registers your models to be displayed in the admin panel, and where admin logic can be placed.

**forms.py**	

Stores the templates for your forms (like the filter used on the homepage) and their logic.
	
**models.py** 

Stores the information for your db models, such as the DataReport model used to store event information

**urls.py**

By default, from the parent mapserver/urls.py, all url requests are passed here.

**views.py**

Your server views. Your urls.py will route a request to render one of these views. This is where most of the server logic is currently located.
	
