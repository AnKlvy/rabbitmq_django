from rest_framework.viewsets import ModelViewSet
from .models import Order
from .serializers import OrderSerializer
from kombu import Connection, Exchange, Producer

from .tasks import initialize_rabbitmq


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # initialize_rabbitmq.apply_async()

    def perform_create(self, serializer):
        """
        Сохраняет заказ и отправляет сообщение о создании.
        """
        order = serializer.save()
        region = self.get_region_from_request()  # Получаем регион из данных запроса
        self.send_order_message(order, region, event="order_created")

    def perform_update(self, serializer):
        """
        Обновляет заказ и отправляет сообщение об обновлении.
        """
        order = serializer.save()
        region = self.get_region_from_request()
        self.send_order_message(order, region, event="order_updated")

    def send_order_message(self, order, region, event):
        """
        Отправляет сообщение о заказе в RabbitMQ через `topic` exchange.
        """
        exchange_name = 'order-topic-exchange'
        exchange = Exchange(exchange_name, type='topic')  # Тип обменника - topic
        routing_key = f"order.{region}"  # Создаём ключ маршрутизации

        # Формируем сообщение
        message = {
            "id": order.id,
            "restaurant": order.restaurant,
            "courier": order.courier,
            "foods": order.foods,
            "status": order.status,
            "event": event,
        }

        # Подключение и публикация
        with Connection("amqp://guest:guest@localhost:5672//") as connection:
            producer = Producer(connection, exchange)
            producer.publish(
                message,
                routing_key=routing_key,
                serializer="json",
                retry=True
            )

    def get_region_from_request(self):
        """
        Получает регион из данных запроса.
        """
        region = self.request.data.get('region')  # Извлечение региона из данных запроса
        if not region:
            raise ValueError("Регион не указан в запросе.")  # Возвращаем ошибку, если региона нет
        return region
