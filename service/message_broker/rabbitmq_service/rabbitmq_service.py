from orders_generator.service.message_broker.message_broker_service import Message_broker_service
import pika

class Rabbitmq_service(Message_broker_service):

    def __init__(self, user, password, host, virtual_host, port):
        super(Rabbitmq_service, self).__init__(user, password, host, virtual_host, port)
        self._connect = pika.BlockingConnection(pika.ConnectionParameters(
                    credentials=pika.PlainCredentials(username=self.user,
                                                      password=self.password),
                    host=self.host,
                    port=self.port,
                    virtual_host=self.virtual_host))

    def open_connection(self):
        if not self._is_connected:
            try:
                self._connect.channel()
                self._is_connected = True
                self._logger.debug(self._connect)
                self._logger.debug(f"Connect to {self.host}:{self.port} is opened")
            except Exception as e:
                self._logger.error(f"{e}. Unable to connect to {self.host}:{self.port}")
        else:
            self._logger.debug(f"Connect to {self.host}:{self.port} is opened")

    def close_connection(self):
        if self._is_connected:
            try:
                self._connect.close()
                self._is_connected = False
                self._logger.debug(f"Connect to {self.host}:{self.port} closed")
            except Exception as e:
                self._logger.error(f"{e}. Unable to connect to {self.host}:{self.port}")
        else:
            self._logger.debug(f"Connect to {self.host}:{self.port} closed")

    def get_channel(self):
        try:
            return self._connect.channel()
        except Exception as e:
            self._logger.error(f"{e}. Unable to get channel in connect {self._connect}")


    def close_channel(self, channel):
        try:
            channel.close()
        except Exception as e:
            self._logger.error(f"{e}. Unable to close channel {channel}")

    def queue_declare(self, queue):
        try:
            self.get_channel().queue_declare(queue=queue)
            self._logger.debug(f"New queue_declare '{queue}'")
        except Exception as e:
            self._logger.error(f"{e}. Unable queue_declare '{queue}'")

    def bind_queue(self, queue_name, exchange_name, routing_key=None):
        try:
            self._connect.channel().queue_bind(queue_name, exchange_name, routing_key=routing_key)
            self._logger.debug(f"Bind {queue_name}.")
        except Exception as e:
            self._logger.error(f"{e}. Unable to bind {queue_name}.")

    def exchange_declare(self, exchange_name, exchange_type):
        try:
            return self._connect.channel().exchange_declare(exchange=exchange_name,
                                                            exchange_type=exchange_type)
        except Exception as e:
            self._logger.error(f"{e}. Unable exchange_declare name = {exchange_name} ; type = {exchange_type}")