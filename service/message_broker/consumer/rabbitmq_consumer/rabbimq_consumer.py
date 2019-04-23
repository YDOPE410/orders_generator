from service.message_broker.consumer.consumer import Consumer
import threading
import pika.exceptions



class Rabbitmq_consumer(Consumer, threading.Thread):
    def __init__(self, queue, message_broker, storage):
        threading.Thread.__init__(self)
        super(__class__, self).__init__(queue, message_broker, storage)
        self._is_stopped = False

    def start(self):
        threading.Thread.start(self)

    def run(self):
        self.logger.debug("Starting consuming")
        self.message_broker.open_connection()
        while not self._is_stopped:
            channel = self.message_broker._get_connection().channel()
            self._consume(channel)
        self.message_broker.close_connection()

    def _consume(self, channel):
        try:
            channel.basic_qos(prefetch_count=1)
            for message in channel.consume(queue=self.queue, auto_ack=True, inactivity_timeout=2):
                method, properties, body = message
                if body == None:
                    self._stop()
                    break
                self.storage.push(body)
            self.logger.debug("Stop consuming")
        except pika.exceptions.AMQPConnectionError as e:
            self._is_stopped = False
            self.logger.error(e)
            self.logger.info("Consumer. Trying reconnect to message broke")
            self.message_broker._reconnect()
            self.logger.info("Consumer. Reconnected to message broker")
        except Exception as e:
            self.logger.error(f"Error while consuming {self.queue}. {e}")

    def _stop(self):
        self._is_stopped = True
