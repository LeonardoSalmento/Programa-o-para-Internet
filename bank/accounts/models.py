from django.db import models

class Account(models.Model):
    owner = models.CharField(max_length=255, blank=True, default= '')
    balance = models.DecimalField(max_digits = 20, decimal_places = 2)
    creation_date = models.DateTimeField()