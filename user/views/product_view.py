from rest_framework import generics
from ..serializers.product_serializer import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from ..models.product import Product
from ..utility import constants
from ..utility.utility_functions import get_object_or_none


class ProductCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        if "name" in request.data and "price" in request.data:
            price = request.data.get("price")
            if price is None or not isinstance(price, (int, float)) or price <= 0:
                res = {"error": "Invalid price. Price must be positive value"}
                res_status = constants.ERROR_STATUS

            else:
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    res = {"success": "Product created successfully"}
                    res_status = constants.CREATE_SUCCESS
                else:
                    # print(serializer.errors.values)
                    # value = serializer.errors.values[0][0]
                    res = {"error": "Invalid data"}
                    res_status = constants.ERROR_STATUS
        else:
            res = {"error": "product name and price are required"}
            res_status = constants.ERROR_STATUS

        return Response(data=res, status=res_status)


class ProductListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        serializer = self.get_serializer(queryset, many=True)

        return Response(
            data={"products": serializer.data}, status=constants.SUCCESS_STATUS
        )


class ProductDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(
                data={"data": serializer.data}, status=constants.CREATE_SUCCESS
            )
        else:
            return Response(
                data={"error": "Product not found"}, status=constants.ERROR_STATUS
            )

    def get_object(self):
        id = self.request.query_params.get("id")
        return get_object_or_none(Product, id=id)


class ProductUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def put(self, request, *args, **kwargs):
        try:
            product_id = request.data["product_id"]
            if "name" in request.data:
                product = get_object_or_none(Product, name=request.data["name"])
                if product is not None and product.id != product_id:
                    return Response(
                        data={"error": "Product with this name already existed"},
                        status=constants.ERROR_STATUS,
                    )
            response = super().partial_update(request, *args, **kwargs)
            if response.status_code == 200:
                response.data = {"success": "Product updated successfully"}
            return response
        except Product.DoesNotExist:
            return Response(
                data={"error": "Product with this id doesn't exist"},
                status=constants.ERROR_STATUS,
            )
        except KeyError:
            return Response(
                data={"error": "product_id field is required"},
                status=constants.ERROR_STATUS,
            )

    def get_object(self):
        id = self.request.data.get("product_id")
        try:
            product = Product.objects.get(id=id)
            return product
        except Product.DoesNotExist:
            raise Product.DoesNotExist


class ProductDeleteView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        if product is None:
            return Response(
                data={"error": "Product with this id does not exist"},
                status=constants.ERROR_STATUS,
            )
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        id = self.request.query_params.get("product_id")
        product = get_object_or_none(Product, id=id)
        return product
