from django.db import models

# Create your models here.
class BikeHireModel(models.Model):
	station_name = models.CharField(max_length = 200)
	