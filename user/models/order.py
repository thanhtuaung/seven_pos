from django.db import models
from ..utility.enums import OrderStatus
from .app_user import AppUser

class Order(models.Model):
    customer = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10)

    class Meta:
        db_table = 'orders'