import pika

from service.message_broker.service.publisher.publisher import Publisher


class Rabbitmq_publisher(Publisher):
    def __init__(self, channel, exchange, routing_key):
        self.channel = channel
        self.exchange = exchange
        self.routing_key = routing_key

    def publish(self, message):
        try:
            self.channel.basic_publish(exchange=self.exchange,
                                       routing_key=self.routing_key,
                                       body=message)
            return True
        except Exception as e:
            print(e)
            return False