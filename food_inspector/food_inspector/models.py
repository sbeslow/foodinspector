from django.db import models


class Search(models.Model):
    searched_term = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now=True)


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=35)
    zip_code = models.CharField(max_length=10)
