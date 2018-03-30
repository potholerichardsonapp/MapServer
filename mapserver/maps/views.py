from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from .forms import SearchForm
from .models import DataReport
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder


# Create your views here.
def search_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            #Get the search params from the valid form
            date_time = form.cleaned_data['date_time']
            z_axis = form.cleaned_data['threshold']
            user_id = form.cleaned_data['user_id']
            event_id = form.cleaned_data['event_id']

            #Package the data that matches the search params
            results = DataReport.objects \
                .filter(generator_gte=user_id) \
                .filter(z_axis__gte=z_axis) \
                .filter(date_time__gte=date_time) \
                .filter(event_id__gte=event_id)


            json_data = []

            #Serialize the data to be returned
            for result in results:
                json_obj = dict(
                    lat=str(result.lat),
                    long=str(result.long),
                    accel=str(result.z_axis),
                    generator=result.generator.pk,
                    date_time = result.date_time,
                    # event_type = result.event_type,
                    # event_id = result.event_id
                )
                json_data.append(json_obj)

                data = json.dumps(json_data, default=date_handler)

            # Return data
            return render(request, 'maps/search.html', {'form': form, 'data': data})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()
        results = ''

    return render(request, 'maps/search.html', {'form': form})

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError