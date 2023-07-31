from django.urls import path
from .views import user_view, product_view, order_view

urlpatterns = [
    path('auth/register/', user_view.register, name='register'),
    path('auth/login/', user_view.login, name='login'),
    
    # Product urls
    path('products/', product_view.ProductListView.as_view(), name='products'),
    path('products/create/', product_view.ProductCreateView.as_view(), name='create-product'),
    path('products/detail/', product_view.ProductDetailView.as_view(), name='detail-product'),
    path('products/update/', product_view.ProductUpdateView.as_view(), name='update-product'),
    path('products/delete/', product_view.ProductDeleteView.as_view(), name='delete-product'),
    
    # Order urls
    path('orders/', order_view.OrderListView.as_view(), name='orders'),
    path('orders/create/', order_view.create_order, name='create-order'),
    path('orders/update/', order_view.OrderUpdateView.as_view(), name='update-order'),
]

