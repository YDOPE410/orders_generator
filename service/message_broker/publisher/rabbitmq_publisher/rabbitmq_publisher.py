from orders_generator.service.message_broker.publisher.publisher import Publisher


class Rabbitmq_publisher(Publisher):

    def __init__(self, channel):
        super(Rabbitmq_publisher, self).__init__(channel)

    def publish(self, exchange, routing_key, message):
        try:
            self.channel.basic_publish(exchange=exchange,
								       routing_key=routing_key,
								       body=message)
        except Exception as e:
            print(f"{e}. Unable to publish to {self.channel}")