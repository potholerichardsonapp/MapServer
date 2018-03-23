# MapServer

Django server for the pothole mapping project.

## Installation

### Pre-reqs
MapServer requires Python 3 and the Django framework.

##### Python3

You might already have Python3 installed. 

In your command line/terminal, type the following commands and see if either one gives you a version of 3.x+

```sh
$ python
```
or
````sh
$ python3
````

If not, download the latest version of python from python.org

NOTE: Any commands given here need to be run with your Python 3 version. So if you get Python 2.x from the 'python' command and Python 3.x from the 'python3' command, be sure to use 'python3' anywhere a command uses 'python'

##### Django
We can install Django using the package manager 'pip' built into your python 3 installation.

```sh
$ pip3 install django
```

### Cloning the project

Navigate to the directory you want to store the code

```sh
$ git clone https://github.com/Clast/MapServer.git
```

### Running the server
Navigate to the directory that has the manage.py file

```sh
$ python3 manage.py runserver
```
You should now be able to access the server at http://127.0.0.1:8000

The admin panel is located at http://127.0.0.1:8000/admin
Check the slack for credentials

## Further reading
https://docs.djangoproject.com/en/2.0/intro/

.