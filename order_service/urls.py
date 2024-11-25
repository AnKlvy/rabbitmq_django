# project/urls.py
from django.urls import path, include

urlpatterns = [
    path('api/', include('orders.urls')),  # Подключение маршрутов Order
]
