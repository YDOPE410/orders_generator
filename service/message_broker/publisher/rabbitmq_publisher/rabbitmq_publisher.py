from orders_generator.service.message_broker.publisher.publisher import Publisher


class Rabbitmq_publisher(Publisher):

    def __init__(self, channel):
        self.channel = channel

    def publish(self, exchange, routing_key, message):
        try:
            self.channel.basic_publish(exchange=exchange,
								       routing_key=routing_key,
								       body=message)
            return True
        except Exception as e:
            self._logger.error(f"{e}. Unable to publish to {self.channel}")
            return False