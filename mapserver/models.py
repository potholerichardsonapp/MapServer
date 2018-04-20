from django.db import models


# Create your models here.
class DataReport(models.Model):
    generator = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    z_axis = models.DecimalField(max_digits=9, decimal_places=6)
    date_time = models.DateTimeField()


class User(models.Model):
    pass