from service.message_broker.consumer.consumer import Consumer
from service.storage.storage import Storage




class Rabbitmq_consumer(Consumer):
    def __init__(self, queue, message_broker, storage):
        super(__class__, self).__init__(queue, message_broker, storage)


    def start(self):
        try:
            self.logger.debug("Starting consuming")
            self.message_broker.open_connection()
            channel = self.message_broker.connection.channel()
            channel.basic_qos(prefetch_count=1)
            for message in channel.consume(queue=self.queue, auto_ack=True, inactivity_timeout=1):
                method, properties, body = message
                if body == None:
                    break
                self.storage.push(body)
            channel.close()
            self.message_broker.close_connection()
            self.logger.debug("Stop consuming")
        except Exception as e:
            self.logger.error(f"Error while consuming {self.queue}. {e}")

