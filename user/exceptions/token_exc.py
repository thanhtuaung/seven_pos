# exceptions.py

from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Call Django REST framework's default exception handler
    response = exception_handler(exc, context)

    if response is not None and response.status_code == 401:
        response.data = {"error": "Invalid token. You do not have permission to perform this action."}

    return response
