from django.db import models
from ..utility.enums import OrderStatus
from .app_user import AppUser

class Order(models.Model):
    customer = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    ordered_date = models.DateTimeField()

    class Meta:
        db_table = 'orders'