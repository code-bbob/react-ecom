from django.urls import path
from .views import OrderAPIView
from . import views

urlpatterns = [ 
    # URL for listing and creating orders (GET and POST)
    path('api/', OrderAPIView.as_view(), name='order-list'),
    path('api/checkout/', views.CheckoutView.as_view(), name="checkout"),
    path('api/cart/', views.CartView.as_view(), name="cart"),
    path('api/cart/update/', views.CartView.as_view(), name="cart-update"),
    path('api/cart/merge/', views.MergeCartView.as_view(), name="cart-merge"),

    # # URL for retrieving, updating, and deleting a specific order (GET, PUT, PATCH, DELETE)
    # path('api/<str:pk>/', OrderAPIView.as_view(), name='order-detail'),
]
