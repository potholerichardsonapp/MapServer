from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import SearchForm
from .models import DataReport

# Create your views here.
def search_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            #Find the data that matches the search params
            z_axis = form.cleaned_data['threshold']
            results = DataReport.objects.filter(z_axis__gte=z_axis)
            # redirect to a new URL:
            return HttpResponseRedirect('index.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()
        results = ''

    return render(request, 'maps/search.html', {'form': form}, {'results': results})