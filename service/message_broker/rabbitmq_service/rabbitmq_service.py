from orders_generator.service.message_broker.message_broker_service import Message_broker_service
import pika

class Rabbitmq_service(Message_broker_service):

    def __init__(self, user, password, host, virtual_host, port):
        super(Rabbitmq_service, self).__init__(user, password, host, virtual_host, port)
        self._connect = None

    def open_connection(self):
        if not self._is_connected:
            try:
                self._connect = pika.BlockingConnection(pika.ConnectionParameters(
					                                    credentials=pika.PlainCredentials(username=self.user,
                                                                                          password=self.password),
					                                    host=self.host,
					                                    port=self.port,
					                                    virtual_host=self.virtual_host))
                self._is_connected = True
                print(self._connect)
                print(f"Connect to {self.host}:{self.port} is opened")
            except Exception as e:
                print(f"{e}. Unable to connect to {self.host}:{self.port}")
        else:
            print(f"Connect to {self.host}:{self.port} is opened")

    def close_connection(self):
        if self._is_connected:
            try:
                self._connect.close()
                self._is_connected = False
                print(f"Connect to {self.host}:{self.port} closed")
            except Exception as e:
                print(f"{e}. Unable to connect to {self.host}:{self.port}")
        else:
            print(f"Connect to {self.host}:{self.port} closed")

    def get_channel(self):
        try:
            return self._connect.channel()
        except Exception as e:
            print(f"{e}. Unable to get channel in connect {self._connect}")


    def close_channel(self, channel):
        try:
            channel.close()
        except Exception as e:
            print(f"{e}. Unable to close channel {channel}")

