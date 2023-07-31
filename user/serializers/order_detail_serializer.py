from rest_framework import serializers
from ..models import OrderDetail

class OrderDetailSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source='product.name')
    product_id = serializers.CharField(source='product.id')
    unit_price = serializers.FloatField(source='product.price')
    subtotal = serializers.SerializerMethodField()
    order_id = serializers.IntegerField(source='order.id')

    def get_subtotal(self, obj):
        return obj.quantity * obj.product.price


    class Meta:
        model = OrderDetail
        fields = ('id', 'order_id','product_id', 'product_name', 'unit_price', 'quantity', 'subtotal')