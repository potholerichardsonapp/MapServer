from django import forms


class SearchForm(forms.Form):
   # start_date = forms.DateTimeField(label='Start Date/Time')
    #end_date = forms.DateTimeField(label='End Date/Time')

    threshold = forms.DecimalField(label='z-axis thresholds', required=False)
    date_time = forms.DateTimeField(label='Date', help_text = '(MM/DD/YYYY)', required=False)



    # CHOICES = (('1', 'Critical',), ('2', 'Warninig',), ('3', 'Watching'))
    # event_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    # user_id = forms.DecimalField(label='user Id', required=False)
    # event_id = forms.DecimalField(label='event Id', required=False)


    ## make this field 'readonly'. toggle touch to designate coordinate? .... SIMPLY CREATE A BUTTON TO SEARCH AREA SHOWN ON SCREEN
    # latitude = forms.DecimalField(label='latitude')
    # longitude = forms.DecimalField(label='longitutde')
