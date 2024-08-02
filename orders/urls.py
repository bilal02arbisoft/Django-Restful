from orders.views import OrderListCreateAPIView
from django.urls import path

urlpatterns = [
    path('', OrderListCreateAPIView.as_view(), name='orders'),

]
