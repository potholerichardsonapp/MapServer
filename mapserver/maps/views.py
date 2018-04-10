from xmlrpc.client import DateTime

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from .forms import SearchForm
from .models import DataReport
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder
import pyrebase
from dateutil import parser
from datetime import datetime, timezone
import pytz


config = {
  "apiKey": "apiKey",
  "authDomain": "pothole-5106f.firebaseapp.com",
  "databaseURL": "https://pothole-5106f.firebaseio.com/",
  "storageBucket": "gs://pothole-5106f.appspot.com"
}

# Create your views here.
def search_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            #Get the search params from the valid form
            z_axis = form.cleaned_data['threshold']
            date_time = form.cleaned_data['date_time']
            # user_id = form.cleaned_data['user_id']
            # event_id = form.cleaned_data['event_id']

            #Package the data that matches the search params
            # results = DataReport.objects \
            #     .filter(z_axis__gte=z_axis) \
                # .filter(date_time__gte=date_time) \
                # .filter(generator_gte=user_id) \
                # .filter(event_id__gte=event_id)


            filters = {}

            if z_axis:
                filters['z_axis__gte'] = z_axis
            if date_time:
                filters['date_time__gte'] = date_time
            results = DataReport.objects.filter(**filters)


            json_data = []

            #Serialize the data to be returned
            if results:
                for result in results:
                    json_obj = dict(
                        lat=str(result.lat),
                        long=str(result.long),
                        accel=str(result.z_axis),
                        generator="",
                        date_time = result.date_time,
                        # event_type = result.event_type,
                        # event_id = result.event_id
                    )
                    json_data.append(json_obj)

                    data = json.dumps(json_data, default=date_handler)
            else:
                data = {}
            # Return data
            return render(request, 'maps/search.html', {'form': form, 'data': data})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()
        results = ''
        update_DB()

    return render(request, 'maps/search.html', {'form': form})

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

    #Get timestamp of latest event and current time
    latest = DataReport.objects.latest('date_time').date_time.timestamp()
    now = datetime.now().timestamp()

    #Fetch events after this time
    posts = db.child("posts").order_by_child("date_time").start_at(latest).end_at(now).get()

    #if not empty, parse date and input into DB
    if posts.pyres:
        posts = dict(posts.val())

        # match firebase data with local server fields
        for post in posts:
            lat = posts[post]['lat']
            long = posts[post]['long']
            z_axis = posts[post]['z_axis']
            date_time = posts[post]['date_time']

            #Convert date_time parse into iso compliant string
            date_time = datetime.utcfromtimestamp(date_time).isoformat()

            # load data report instance with data fields
            datareport = DataReport(
                lat=lat, long=long, z_axis=z_axis,  date_time=date_time)

            # save the datareport instance
            datareport.save()