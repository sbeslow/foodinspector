from django.db import models


class Search(models.Model):
    searched_term = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now=True)
