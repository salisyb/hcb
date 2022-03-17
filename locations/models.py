from django.db import models

# Create your models here.


class Locations(models.Model):
    name = models.CharField(max_length=200)
    picture_url = models.URLField()
    Locations = models.CharField(max_length=300)
    descriptions = models.TextField()
