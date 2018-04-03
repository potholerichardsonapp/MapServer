from django_filters


class SearchFilter(django_filters.FilterSet):
    # date_time = django_fiters.DateTimeFilter()
    # threshold = django_filters.NumberFilter(name='z-axis')
    # user_id = django_filters.NumberFilter(name='generator')
    # event_id = django_filters.NumberFilter()
    #
    # location_coordinate = django_filters.DecimalFilter(lookup_map='icontains')

    class Meta:
        model = DataReport
        fields = ['lat', 'long', 'accel', 'generator', 'date_time', 'event_type', ]