from rest_framework import generics
from ..serializers.order_serializer import OrderSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from ..models.order import Order
from ..utility import constants
from rest_framework.decorators import (
    permission_classes,
    authentication_classes,
    api_view,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_order(request: Request):
    data = request.data
    if not ("customer_id" in data and "product_ids" in data and "status" in data):
        res = {'error': 'customer_id, product_ids and status fields are required'}
        res_status = constants.ERROR_STATUS
    else:
        order_data = {
            "customer": data['customer_id'],
            "status": data['status'],
        }

        order_serializer = OrderSerializer(data=order_data)

        if order_serializer.is_valid():
            res = None
            res_status = constants.CREATE_SUCCESS

            

        else:
            res = order_serializer.errors
            res_status = constants.ERROR_STATUS

        

    return Response(data=res,status=res_status)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if response.status_code == 200:
            response.data = {"orders": response.data}
        return response
