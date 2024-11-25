# orders/models.py
from django.db import models

class Order(models.Model):
    restaurant = models.CharField(max_length=255)
    courier = models.CharField(max_length=255)
    foods = models.JSONField()  # Для хранения списка продуктов
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Order from {self.restaurant} (Status: {self.status})"
