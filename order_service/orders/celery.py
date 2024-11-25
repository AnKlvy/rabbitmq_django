# project/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from orders.tasks import initialize_rabbitmq

# Устанавливаем настройки для Celery, включая настройку брокера RabbitMQ
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orders.settings')

app = Celery('orders')

# Используем RabbitMQ в качестве брокера
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загружаем задачи из всех зарегистрированных приложений Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# Настройки Celery для RabbitMQ
# app.conf.broker_url = 'amqp://guest:guest@localhost//'
# app.conf.accept_content = ['json']
# app.conf.task_serializer = 'json'
# app.conf.result_backend = 'rpc://'
# app.conf.task_default_exchange_type = 'direct'
# app.conf.task_default_exchange = 'order-topic-exchange'  # Название обменника
# app.conf.task_default_routing_key = 'order.general'  # Ключ маршрутизации по умолчанию

