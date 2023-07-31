from rest_framework import serializers
from ..models import OrderDetail

class OrderDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'