from django.shortcuts import render
from .forms import SearchForm
from .models import DataReport
import json
import pyrebase
from datetime import datetime

# Config for firebase DB.
config = {
    "apiKey": "apiKey",
    "authDomain": "pothole-5106f.firebaseapp.com",
    "databaseURL": "https://pothole-5106f.firebaseio.com/",
    "storageBucket": "gs://pothole-5106f.appspot.com"
}


# Search index view
def search_form(request):
    # When the form is submitted, incoming request will be a POST
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)

        # Get the search params from the valid form
        if form.is_valid():
            z_axis = form.cleaned_data['threshold']
            date_time = form.cleaned_data['date_time']
            user = form.cleaned_data['users']

            # Query for results using retrieved data
            filters = {}

            if z_axis:
                filters['z_axis__gte'] = z_axis
            if date_time:
                filters['date_time__gte'] = date_time
            if user != "All":
                filters['generator'] = user

            results = DataReport.objects.filter(**filters)

            # Serialize the data to be returned so we can pass it to front end
            json_data = []
            if results:
                for result in results:
                    json_obj = dict(
                        lat=str(result.lat),
                        long=str(result.long),
                        accel=str(result.z_axis),
                        generator=result.generator,
                        date_time=result.date_time,
                    )
                    json_data.append(json_obj)

                    data = json.dumps(json_data, default=date_handler)
            else:
                data = {}

            # Return data
            return render(request, 'search.html', {'form': form, 'data': data})

    # if it's a GET request, probably the initial visit. Generate an empty form and update DB.
    else:
        form = SearchForm()
        results = ''
        update_DB()

    return render(request, 'search.html', {'form': form})


def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError


def update_DB():
    # initialize the pyrebase library
    firebase = pyrebase.initialize_app(config)

    # create a database instance
    db = firebase.database()

    # Get timestamp of latest event and current time
    try:
        latest = DataReport.objects.latest('date_time').date_time.timestamp()
    except DataReport.DoesNotExist:
        latest = 0

    now = datetime.now().timestamp()

    # Fetch events after this time
    posts = db.child("posts").order_by_child("date_time").start_at(latest).end_at(now).get()

    # if not empty, parse date and input into DB
    if posts.pyres:
        posts = dict(posts.val())

        # match firebase data with local server fields
        for post in posts:
            lat = posts[post]['lat']
            long = posts[post]['long']
            z_axis = posts[post]['accelerometerZ']
            date_time = posts[post]['date_time']
            gen_field = posts[post]['id']

            # Convert date_time parse into iso compliant string
            date_time = datetime.utcfromtimestamp(date_time).isoformat()

            # load data report instance with data fields
            datareport = DataReport(
                lat=lat, long=long, z_axis=z_axis, date_time=date_time, generator=gen_field)

            # save the datareport instance

            if lat != 0 and long != 0:
                datareport.save()
