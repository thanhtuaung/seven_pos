from rest_framework import generics

class BaseListView(generics.ListAPIView):

    key_name = ''

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if response.status_code == 200:
            response.data = {self.key_name: response.data}
        return response