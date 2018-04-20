# Getting Started 

On this page, we'll talk about getting your development environment set up and how to run the server locally


## Requirements

- [Python 3](https://www.python.org/download/releases/3.0/)
- [git](https://git-scm.com/)

If using a windows machine, you'll want to make sure that your PATH environment variable is set up so you can run these tools from the command line.

**Optional**: The creator of this documentation uses [CMDER](http://cmder.net/) which is a console emulation tool allowing unix style commands in windows, and comes prepackaged with a git install.


## Cloning the project

From the command line, navigate to the directory you want to clone the project.

	git clone https://github.com/potholerichardsonapp/MapServer.git
	
## Virtual Environment


Python virtual environments, managed by venv, are set up for installing packages and running programs in a way that isolates them from other packages installed on the rest of the system. 

Because this server requires several external python packages, it's recommended to use a venv to manage them and to make collaboration easier.

If you don't already have venv installed

	pip install virtualenv
	
Once installed, you can create a new virtual environment in the directory of your choice with:

	virtualenv ENVName
	
On windows, to activate the virtual environment you can use:

	/path/to/env/Scripts/activate
	
When activated, your command line will appear like:

	(ENVName)$ 
	


## Installing required python packages

If you're using your virtual environment, make sure that's activated.

In the cloned project directory, you'll notice a file called 'requirements.txt'. This is a generated file from pip showing all currently installed packages in your venv.

You can batch install these packages using

	(ENVName)$ pip install -r path/to/requirements.txt

## Initial database migrations

The first time you run the server, you may need to make some database migrations to construct the database schema.

From the project directory you can run:

	(ENVName)$ python manage.py migrate
	(ENVName)$ python manage.py makemigrations


## Running the server

From the project directory containing manage.py

	(ENVName)$ python manage.py runserver
	
Your server should now be running and you'll be able to access it at [localhost:8000](localhost:8000)


	
	
