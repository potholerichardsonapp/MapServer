from django import forms


class SearchForm(forms.Form):
   # start_date = forms.DateTimeField(label='Start Date/Time')
    #end_date = forms.DateTimeField(label='End Date/Time')
    threshold = forms.DecimalField(label='z-axis thresholds')
