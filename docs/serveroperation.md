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

All backend data is returned in a single object to be unpacked later:
	var data = {{data | safe}};

The Google Maps API is used: https://developers.google.com/maps/documentation/javascript/reference/3.exp/

Make sure that API source and key is valid and correct:

	<script type="text/javascript" src="http://maps.googleapis.com/maps/api/js?	libraries=visualization&language=fra&amp;sensor=false"></script>

Map and streetview are implemented as 2 different divs, in order to make CSS changes more maneagable. To edit the visuals, just find the id tag in the CSS section of `search.html`. 

# Json Unpacking
Each location is saved in an 2D array, using the key value pair structure of a JSON object. Access as nodes[Node][Attribute]:

      var nodes = data.map(function (object) {
        return [object["lat"], object["long"], object["accel"], object["generator"], object["date_time"]]
      });
 
In this specfic case, [node][1] - Lat, [node][2] -lng, [node][3] acceleration, etc..
To update the key value pairs, simply replace all the keys in the quotes to match with the keys given by the backend.
**Note**: An understanding of the Javascript `map` function is pivotal to understand how it update in the future
    
   
# Google Markers
All node attributes (Streetview, Infobox, etc..) are implemented in the one single loop. Each node will be a marker, with location attributes being its only values.
Each node is saved into Google Maps Marker data types, and pointed/added at the local `map` object in the specific instance:

        var marker = new google.maps.Marker({
          position: position,
          map: map,
        });
	
# Info Box
An info box is implemented with an event listener on the the marker created for that specfic location. The infobox acts as a means of adding more attributes to that marker. Specifcally, `setContent` adds more values to it. To edit whats in the info box, simply do a string concantantion on what you want it to say. **HTML can be added, and viewed as such**. 

            infowindow.setContent('<h3><strong>' + nodes[i][4] + '</strong></h3>' +
              '<p>' + 'lat: ' + nodes[i][0] + ', long: ' + nodes[i][1] + '</p>' +
              '<p>' + 'accel: ' + nodes[i][2] + '</p>' +
              '<p>' + 'generator: ' + nodes[i][3] + '</p>'
            );
	    
# Streetview	    
Streetview nodes are added the street view object, all location data populated by the 2D array. The location attribute needs to be filled with valide locations, and a radius value (how far from the initial location to find alternate view) in the case that it is not valid

            sv.getPanorama({
              location: {
                lat: Number(nodes[i][0]),
                lng: Number(nodes[i][1])
              },
              radius: 50
            }, processSVData);
	    
If you would like to customize how the Streetview looks on load, edit the following the function from the callback:

    function processSVData(data, status) {
      if (status === 'OK') {

        panorama.setPano(data.location.pano);
        panorama.setPov({
          heading: 270,
          pitch: 0
        });

        panorama.setVisible(true);

      } else {
        console.error('Street View data not found for this location.');
      }
    }


# Map Autozoom
The autozoom feature (where the map will zoom out in order to get as many markers in view) is then implmented by adding bounds, using the latitude and longitiude (latlng) populated by the 2D array. The `fitBounds` function simply needs at latitude and longitude to add the bounding attribute to the local map instance.

      var latlngbounds = new google.maps.LatLngBounds();
      for (var i = 0; i < latlng.length; i++) {
        latlngbounds.extend(latlng[i]);
      }
      map.fitBounds(latlngbounds);
      
     
# Heatmap
The locations are then added to the Heatmap object using Javascripts `map` function. `object` is the current iteration of node in the 2D, as this is how `map` goes through iterable object. `map` returns an array specfied by what is returned. The heatmap `data` key only needs an arrau of LatLng objects (created by the `LatLng` function).

      heatmap = new google.maps.visualization.HeatmapLayer({
        data:  nodes.map(function(object){return new google.maps.LatLng(object[0], object[1])}),
        map: map
      });

# Floating Bar
To add functionality floating bar, just add a button tag with an accomping `onclick` function to give it more functionality
Ex.
 	<div id="floating-panel">
  	<button onclick="toggleHeatmap()">Toggle Heatmap</button>
To edit the size and looks of the bar, find the id in the CSS section to update it.
