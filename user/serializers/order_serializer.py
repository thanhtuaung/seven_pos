from rest_framework import serializers
from ..models.order import Order
from ..serializers.order_detail_serializer import OrderDetailSerializer

class OrderSerializer(serializers.ModelSerializer):

    customer_id = serializers.IntegerField(source='customer.id')
    customer_name = serializers.CharField(source='customer.username')
    total_amount = serializers.SerializerMethodField()
    order_details = serializers.SerializerMethodField()

    def get_total_amount(self, obj: Order):
        total = 0
        
        for detail in obj.orderdetail_set.all():
            total += detail.product.price * detail.quantity
        return total
    
    def get_order_details(self, obj: Order):
        details = obj.orderdetail_set.all()
        detail_serializer = OrderDetailSerializer(details, many=True)
        return detail_serializer.data

    class Meta:
        model = Order
        fields = ('id', 'customer_id', 'customer_name', 'ordered_date', 'status', 'total_amount', 'order_details')
        