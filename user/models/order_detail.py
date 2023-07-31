from django.db import models
from ..models import Order

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)