import time
import pika
import pika.exceptions
from service.message_broker.message_broker import Message_broker
from constant.constants_reconnect import *
from service.message_broker.publisher.rabbitmq_publisher.rabbitmq_publisher import Rabbitmq_publisher
from service.message_broker.consumer.rabbitmq_consumer.rabbimq_consumer import Rabbitmq_consumer


class Rabbitmq_service(Message_broker):
    def __init__(self, user, password, host, virtual_host, port):
        super(Rabbitmq_service, self).__init__(user, password, host, virtual_host, port)
        self.publishers = dict()
        self.consumers = dict()
        self.connection = None


    def open_connection(self):
        try:
            self.logger.debug(f"Trying open connection to message broker")
            self.connection = self._open_connection()
            self.logger.debug(f"Connected to message broker")
        except pika.exceptions.AMQPError as e:
            self.logger.error(f"Cant connect to message broker")
            self.logger.error(e)
            self._reconnect()
            self.logger.debug(f"Reconnected to message broker")


    def _open_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(
				credentials=pika.PlainCredentials(username=self.user, password=self.password),
				host=self.host,
				port=self.port,
				virtual_host=self.virtual_host))

    def close_connection(self):
        try:
            self.connection.close()
            self.logger.debug("Message broker closed")
        except pika.exceptions.AMQPError as e:
            self.logger.error(f"Cant close message broker. {e}")

    def _reconnect(self):
        self.logger.debug(f"Trying reconnect to message broker")
        for i in range(NUMBERS_TO_RECONNECT):
            try:
                self.connection = self._open_connection()
                return
            except Exception as e:
                self.logger.error(f"Reconnect failed. {e}")
                if i + 1 < NUMBERS_TO_RECONNECT:
                    self.logger.info(f"{RECONNECT_TIMEOUT} sec to reconnect")
                    time.sleep(RECONNECT_TIMEOUT)
        self.logger.fatal(f"Cant connect to message broker after {NUMBERS_TO_RECONNECT} reconnects")
        exit(1)

    def _queue_bind(self, channel, queue, exchange, routing_key):
        try:
            channel.queue_bind(queue=queue,
                               exchange=exchange,
                               routing_key=routing_key)
        except Exception as e:
            self.logger.error(f"Cant bind queue. {e}")

    def _queue_declare(self, channel, queue, passive=False, durable=False, exclusive=False, auto_delete=False):
        try:
            channel.queue_declare(queue=queue,
                                  passive=passive,
                                  durable=durable,
                                  exclusive=exclusive,
                                  auto_delete=auto_delete)
        except Exception as e:
            self.logger.error(f"Cant declare queue. {e}")

    def _exchange_declare(self, channel, exchange=None, exchange_type='direct',
                          passive=False, durable=False, auto_delete=False):
        try:
            channel.exchange_declare(exchange=exchange,
                                     exchange_type=exchange_type,
                                     passive=passive,
                                     durable=durable,
                                     auto_delete=auto_delete)
        except Exception as e:
            self.logger.error(f"Cant declare exchange. {e}")

    def _setup_consumer(self, channel, queue):
        self._queue_declare(channel=channel, queue=queue)

    def _setup_publisher(self, channel, exchange, exchange_type, queue, routing_key):
        self._exchange_declare(channel=channel, exchange=exchange, exchange_type=exchange_type)
        self._queue_declare(channel=channel, queue=queue)
        self._queue_bind(channel=channel, queue=queue, exchange=exchange, routing_key=routing_key)

    def add_publisher(self, publisher_name, exchange, exchange_type, queue, routing_key):
        try:
            channel = self.connection.channel()
            self._setup_publisher(channel, exchange, exchange_type, queue, routing_key)
            publisher = Rabbitmq_publisher(channel, exchange, routing_key)
            self.publishers[publisher_name] = publisher
            self.logger.debug(f"Added publisher with name {publisher_name}. Publisher can publish to {queue}."
                              f"exchange = {exchange}; exchange_type = {exchange_type}; routing_key = {routing_key}")
        except Exception as e:
            self.logger.error(f"Cant add publisher. {e}")


    def add_consumer(self, consumer_name, queue, storage):
        try:
            channel = self.connection.channel()
            self._setup_consumer(channel, queue)
            consumer = Rabbitmq_consumer(queue, self, storage)
            self.consumers[consumer_name] = consumer
            self.logger.debug(f"Added consumer with name {consumer_name}. Consume queue = {queue}.")
        except Exception as e:
            self.logger.error(f"Cant add consumer. {e}")

