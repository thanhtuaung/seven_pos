from django.db import models
from ..models import Order, Product

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()

    class Meta:
        db_table = 'order_details'
