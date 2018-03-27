from django import forms


class SearchForm(forms.Form):
   # start_date = forms.DateTimeField(label='Start Date/Time')
    #end_date = forms.DateTimeField(label='End Date/Time')
    threshold = forms.DecimalField(label='z-axis thresholds')
    userId = forms.DecimalField(label='user Id')
    eventId = forms.DecimalField(label='event Id')

    ## make this field 'readonly'. toggle touch to designate coordinate? .... SIMPLY CREATE A BUTTON TO SEARCH AREA SHOWN ON SCREEN
    # latitude = forms.DecimalField(label='latitude')
    # longitude = forms.DecimalField(label='longitutde')
