from rest_framework import generics
from ..serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderDetailCreateSerializer,
)
from rest_framework.request import Request
from rest_framework.response import Response
from datetime import datetime
from ..models import Product, Order, AppUser
from ..utility import constants
from .view_utility.list_view import BaseListView
from ..utility.utility_functions import get_object_or_none
from rest_framework.decorators import (
    permission_classes,
    authentication_classes,
    api_view,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_order(request: Request):
    data = request.data
    if not ("customer_id" in data and "products" in data and "status" in data):
        res = {"error": "customer_id, products and status fields are required"}
        res_status = constants.ERROR_STATUS
    else:
        order_data = {
            "customer": data["customer_id"],
            "ordered_date": datetime.now(),
            "status": data["status"],
        }

        customer = get_object_or_none(AppUser, id=data["customer_id"])

        if customer is None:
            return Response(
                data={"error": "customer with this id doesn't exist"},
                status=constants.ERROR_STATUS,
            )

        order_serializer = OrderCreateSerializer(data=order_data)
        detail_serializers = []

        if order_serializer.is_valid():
            for product in data["products"]:
                product_id = product["id"]
                quantity = product["quantity"]
                product = get_object_or_none(Product, id=product_id)
                if product is None:
                    res = {"error": f"Product with id({product_id}) does not exist"}
                    res_status = constants.ERROR_STATUS
                    break

                if (
                    quantity is None
                    or not isinstance(quantity, (int, float))
                    or quantity <= 0
                ):
                    print(f"Is instance {isinstance(quantity, float)}")
                    res = {
                        "error": "Invalid quantity.Quantity must be positive greater than zero"
                    }
                    res_status = constants.ERROR_STATUS
                    break

                detail_seri = OrderDetailCreateSerializer(
                    data={"product": product_id, "quantity": quantity}
                )
                detail_serializers.append(detail_seri)
            else:
                order: Order = order_serializer.save()

                for seri in detail_serializers:
                    seri.initial_data["order"] = order.id
                    if seri.is_valid():
                        seri.save()

                res = None
                res_status = constants.CREATE_SUCCESS
        else:
            res = order_serializer.errors
            res_status = constants.ERROR_STATUS

    return Response(data=res, status=res_status)


class OrderListView(BaseListView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    key_name = 'orders'


class OrderUpdateView(generics.UpdateAPIView):
    
    def put(self, request, *args, **kwargs):

        order_id = request.data.get('order_id')
        if order_id:
            order = self.get_object()
            if order is None:
                res = {"error": "Order with this id doesn't exist"}
                res_status = constants.ERROR_STATUS
            else:
                response = super().partial_update(request, *args, **kwargs)
                return response

        else:
            res = {"error": "order_id field is required"}
            res_status = constants.ERROR_STATUS
        return Response(data=res, status=res_status)
    
    def get_object(self):
        id = self.request.get('order_id')
        return get_object_or_none(Order, id=id)
