# The lifecycle of a user

#Initial navigation

When a user navigates to your website, the Django webserver will first look at it's mapserverproj/urls.py to see if the page the user is attempting to reach has a corresponding view to render.

In our project, any non /admin pages will redirect it's search to the mapserver/urls.py.

	mapserver/urls.py
	
	urlpatterns = [
    path('', views.search_form, name='search_form'),
	]
	
Here, for a blank match. The server will call the search_form view located in mapserver/views.py

#The matching view

In views.py, search_form is where most of the logic for the server currently exists. When search_form is called, the browser *request* is passed to the view containing it's type (GET, POST, etc.) and any associated data.

The search_form itself reacts depending on the request being passed in.

If the request is a GET (indicating that the user is visiting this page without submitting the search form):

	Get the search form from forms.py
	Set the returning data object to empty
	Sync the firebase database (Note, if the unsynced data is large, it may appear the page has stalled while this loads)
	render the search.html template, passing our data object

If the request is a POST (indicating a form submission):

	Collect the submitted form data from the users request
	Check to see that the form validation was successful
	Parse the form data
	Perform a query on our local database
	Parse the returned results to our data object
	render the search.html template, passing our data object

You can check the code to see the specifics of how these are performed.

#The form

You probably noticed during the view logic that we rendered a searh form. 

This can be found in the forms.py file.

	class SearchForm(forms.Form):

		choices = []
		user_choices = DataReport.objects.values('generator').distinct()

		choices.append(("All", "All"))
		for x in user_choices:
			choices.append( (x['generator'],x['generator']) )

		threshold = forms.DecimalField(label='z-axis thresholds', required=False)
		date_time = forms.DateTimeField(label='Date', required=False, widget=forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'}))
		users = forms.CharField(label='User', widget=forms.Select(choices=choices), required=False)

		#This initializer is required to update users field on each form load, not just when server is started
		#If you have a dynamic field, be sure to add logic here.
		def __init__(self, *args, **kwargs):
			super(SearchForm, self).__init__(*args, **kwargs)
			choices = []
			user_choices = DataReport.objects.values('generator').distinct()

			choices.append(("All", "All"))
			for x in user_choices:
				choices.append((x['generator'], x['generator']))

			self.fields['users'] = forms.ChoiceField(
				choices=choices)
		
The form class defines what fields you want to display on the form, their validators (if any), and any other logic that needs to be performed.

In it's current state, we have three fields which are used to query our data, but more can be added:

	threshold = forms.DecimalField(label='z-axis thresholds', required=False)
    date_time = forms.DateTimeField(label='Date', required=False, widget=forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'}))
    users = forms.CharField(label='User', widget=forms.Select(choices=choices), required=False)

The users field loads all the distinct "generators" from the database and displays them. For dynamic fields like these, by default they're only loaded once when the server loads. We have overridden this behavior in the initializer for the form object.

If you add more dynamic fields, you must do the same if you want it to load everytime the form is called.

#The template

When you render a page from the view, you are calling a template from the mapserver/templates folder, and usually passing some data into it like the form objects to render and any data object that needs to be exposed to the front end logic.

------

# Front End

'Test Code'

