from kombu import Connection, Exchange, Queue
from celery import shared_task
from kombu.exceptions import KombuError


@shared_task
def initialize_rabbitmq():
    """
    Создаёт обменники и очереди для RabbitMQ.
    """
    try:
        # Подключаемся к RabbitMQ
        with Connection(
                "amqp://guest:guest@rabbitmq:5672//") as connection:  # Локальный хост заменён на docker service 'rabbitmq'
            print("RabbitMQ initialization task is running")
            # Создаём очереди для Topic Exchange
            with connection.channel() as channel:  # Открываем канал для взаимодействия

                # Создаём Topic Exchange через Kombu Exchange
                exchange = Exchange('order-topic-exchange', type='topic', durable=True, auto_delete=False)
                # Сначала объявляем Exchange
                exchange.declare(channel)
                print(f"Exchange 'order-topic-exchange' created")

                for region in ['almaty', 'aqtobe']:
                    # Создаём очередь с привязкой к exchange и routing_key
                    queue = Queue(f'order-topic-q-{region}', exchange=exchange, routing_key=f'order.{region}',
                                  durable=True, auto_delete=False)
                    # Объявляем очередь
                    queue.declare(channel)
                    print(f"Queue created: order-topic-q-{region}")

                print("RabbitMQ initialization completed")
    except KombuError as e:
        print(f"Error initializing RabbitMQ: {e}")
    except Exception as e:
        print(f"Unexpected error initializing RabbitMQ: {e}")
