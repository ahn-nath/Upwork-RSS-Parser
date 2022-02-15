from django.db import models


# Create your models here.

class Teacher(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField()


class CustomRequirements(models.Model):
    keywords = models.CharField(max_length=80)
    hourly_rate = models.IntegerField()
    budget = models.IntegerField()
    to_email = models.EmailField()

