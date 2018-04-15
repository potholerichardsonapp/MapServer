from django import forms
from .models import DataReport


class SearchForm(forms.Form):
   # start_date = forms.DateTimeField(label='Start Date/Time')
    #end_date = forms.DateTimeField(label='End Date/Time')

    choices = []
    user_choices = DataReport.objects.values('generator').distinct()

    choices.append(("All", "All"))
    for x in user_choices:
        choices.append( (x['generator'],x['generator']) )

    threshold = forms.DecimalField(label='z-axis thresholds', required=False)
    date_time = forms.DateTimeField(label='Date', required=False, widget=forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'}))
    users = forms.CharField(label='User', widget=forms.Select(choices=choices), required=False)


    # CHOICES = (('1', 'Critical',), ('2', 'Warninig',), ('3', 'Watching'))
    # event_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    # user_id = forms.DecimalField(label='user Id', required=False)
    # event_id = forms.DecimalField(label='event Id', required=False)


    ## make this field 'readonly'. toggle touch to designate coordinate? .... SIMPLY CREATE A BUTTON TO SEARCH AREA SHOWN ON SCREEN
    # latitude = forms.DecimalField(label='latitude')
    # longitude = forms.DecimalField(label='longitutde')


    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        choices = []
        user_choices = DataReport.objects.values('generator').distinct()

        choices.append(("All", "All"))
        for x in user_choices:
            choices.append((x['generator'], x['generator']))

        self.fields['users'] = forms.ChoiceField(
            choices=choices)