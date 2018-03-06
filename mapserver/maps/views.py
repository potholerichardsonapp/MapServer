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
            z_axis = form.cleaned_data['threshold']

            #Package the data that matches the search params
            results = DataReport.objects.filter(z_axis__gte=z_axis)

            json_data = []

            #Serialize the data to be returned
            for result in results:
                json_obj = dict(
                    lat = str(result.lat),
                    long = str(result.long),
                    accel = str(result.z_axis),
                    generator = result.generator.pk,
                    date_time = result.date_time,

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