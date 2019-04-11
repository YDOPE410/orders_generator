import pika
from service.message_broker.service.message_broker import Message_broker
from service.message_broker.service.publisher.rabbitmq_publisher.rabbitmq_publisher import Rabbitmq_publisher
from service.message_broker.service.consumer.rabbitmq_consumer.rabbitmq_consumer import Rabbitmq_consumer


class Rabbitmq_service(Message_broker):
    def __init__(self, connection):
        self.connection = connection
        self.publishers = dict()
        self.consumers = dict()

    def add_publisher(self, channel_number, publisher_name, exchange, exchange_type, queue, routing_key):
        channel = self.connection.get_channel(channel_number)
        self._setup_publisher(channel, exchange, exchange_type, queue, routing_key)
        publisher = Rabbitmq_publisher(channel, exchange, routing_key)
        self.publishers[publisher_name] = publisher

    def add_consumer(self, channel_number, consumer_name, queue):
        channel = self.connection.connection.channel()
        self._setup_consumer(channel,
                             queue)
        consumer = Rabbitmq_consumer(queue, channel)
        self.consumers[consumer_name] = consumer

    def get_channel(self, channel_number):
        return self.connection.get_channel(channel_number)

    def start_consume(self, consumer_name):
        self.consumers[consumer_name].start_consuming()

    def stop_consume(self, consumer_name):
        pass

    def _setup_publisher(self, channel, exchange, exchange_type, queue, routing_key):
        self._exchange_declare(channel, exchange=exchange, exchange_type=exchange_type)
        self._queue_declare(channel, queue=queue)
        self._queue_bind(channel=channel, exchange=exchange, routing_key=routing_key, queue=queue)


    def _setup_consumer(self, channel, queue):
        self._queue_declare(channel=channel,
                            queue=queue)

    def _exchange_declare(self, channel, exchange, exchange_type):
        try:
            channel.exchange_declare(exchange=exchange,
                                     exchange_type=exchange_type)
        except Exception as e:
            print(e)

    def _queue_declare(self, channel, queue):
        # try:
        channel.queue_declare(queue=queue)
        # except Exception as e:
        #     print(e)

    def _queue_bind(self, channel, queue, exchange, routing_key):
        try:
            channel.queue_bind(queue=queue,
                               exchange=exchange,
                               routing_key=routing_key)
        except Exception as e:
            print(e)