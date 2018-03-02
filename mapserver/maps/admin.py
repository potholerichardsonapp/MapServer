from django.contrib import admin

from maps.models import DataReport
from maps.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', ) #You can use 'pk' or 'id'
    list_display_links = ('id', )   #the same here - 'pk' or 'id'


admin.site.register(DataReport)
admin.site.register(User, UserAdmin)

