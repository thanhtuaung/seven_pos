from rest_framework import serializers
from ..models import Order

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'