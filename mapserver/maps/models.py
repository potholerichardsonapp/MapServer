from django.db import models


# Create your models here.
class DataReport(models.Model):
    generator = models.ForeignKey('User',  on_delete=models.CASCADE, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    z_axis = models.DecimalField(max_digits=9, decimal_places=6)
    event_type = models.CharField(max_length=200)
    date_time = models.DateTimeField()

    def return_user(self):
        return self.generator
    def return_lat(self):
        return self.lat
    def return_long(self):
        return self.long
    def return_accel(self):
        return self.z_axis
    def return_event_type(self):
        return self.event_type
    def return_date_time(self):
        return self.date_time

    def __str__(self):
        list = [self.return_lat(), self.return_long(), self.return_accel()
                , self.return_event_type(), self.date_time]

        mystring = ""

        for x in list:
            mystring += str(x)
            mystring += '\n'

        return mystring

class User(models.Model):
    pass