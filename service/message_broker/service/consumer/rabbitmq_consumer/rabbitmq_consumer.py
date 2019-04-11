from proto.serializer.order_serializer.order_serializer import Order_serializer


class Rabbitmq_consumer():
    def __init__(self, queue, channel):
        self.queue = queue
        self.channel = channel

    def start_consuming(self):
        self._consume(self.queue)
        self.channel.start_consuming()

    def _consume(self, queue, auto_ack=True, *args, **kwargs):
        self.channel.basic_consume(queue=queue, on_message_callback=self._callback, auto_ack=auto_ack)

    def _callback(self, method, properties, body, *args, **kwargs):
        if body == "stop":
            print(body)
            self.channel.stop_consuming()
        else:
            print((Order_serializer.deserialize(body)).id)
