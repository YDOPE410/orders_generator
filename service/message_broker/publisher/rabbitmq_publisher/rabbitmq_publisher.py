from service.message_broker.publisher.publisher import Publisher
import pika

class Rabbitmq_publisher(Publisher):
    def __init__(self, channel, exchange, routing_key):
        super(__class__, self).__init__()
        self.channel = channel
        self.exchange = exchange
        self.routing_key = routing_key

    def publish(self, message):
        try:
            self.channel.basic_publish(exchange=self.exchange,
                                       routing_key=self.routing_key,
                                       body=message,
                                       properties=pika.BasicProperties(delivery_mode=2))
            return True
        except Exception as e:
            self.logger.error(f"Cant publish {message}. {e}")
            return False