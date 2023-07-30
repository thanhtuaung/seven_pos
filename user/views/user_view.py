from ..serializers.user_serializer import AppUserSerializer
from ..models.app_user import AppUser
from rest_framework import request, response
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password


success_status = status.HTTP_200_OK
error_status = status.HTTP_400_BAD_REQUEST


@api_view(["POST"])
def register(request: request.Request):
    try:
        request_data = request.data

        username = request_data["username"]
        email = request_data["email"]
        password = request_data["password"]

        hashed_password = make_password(password=password)
        request_data["password"] = hashed_password

        serialzier = AppUserSerializer(data=request.data)
        if serialzier.is_valid():
            user = serialzier.save()
            token: RefreshToken = RefreshToken.for_user(user)
            access_token = str(token.access_token)

            res = serialzier.data
            del res['password']
            res["access_token"] = access_token
            res_status = status.HTTP_201_CREATED

        else:
            res = serialzier.error_messages
            res_status = error_status

    except KeyError:
        res = {"error": "username, email, password fields are required"}
        res_status = error_status

    return response.Response(data=res, status=res_status)


@api_view(["GET"])
def login(request: request.Request):
    try:
        email = request.data["email"]
        password = request.data["password"]

        user: AppUser = AppUser.objects.get(email=email)
        if user and user.check_password(password):
            token = RefreshToken.for_user(user=user)
            access_token = str(token.access_token)
            res = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "access_token": access_token,
            }
            res_status = success_status

        else:
            res = {"error": "Incorrect password"}
            res_status = error_status

    except KeyError:
        res = {"error": "email and password are required"}
        res_status = error_status

    except AppUser.DoesNotExist:
        res = {"error": "user with this email does not exist"}
        res_status = error_status

    return response.Response(data=res, status=res_status)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def products(request: request.Request):
    return response.Response(
        data={
            "user": {
                "id": request.user.id,
                "email": request.user.email,
                "password": request.user.password
            }
        },
        status=success_status,
    )
