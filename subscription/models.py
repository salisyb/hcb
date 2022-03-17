from django.db import models

# Create your models here.


class Subscription(models.Model):
    type = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    duration = models.IntegerField()
    books_access = models.IntegerField()
    image_access = models.IntegerField()
    videos_access = models.DurationField()
