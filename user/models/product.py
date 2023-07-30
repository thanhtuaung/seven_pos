from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField()

    class Meta:
        db_table = 'products'