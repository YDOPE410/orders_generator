import time
import pika
from constant import constants_reconnect
from service.message_broker.message_broker_connection.message_broker_connection import Message_broker_connection

class Rabbitmq_connection(Message_broker_connection):

    def __init__(self, user, password, host, virtual_host, port):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.virtual_host = virtual_host
        self.connection = None


    def open_connection(self):
        try:
            self.connection = self._open_connection()
        except Exception as e:
            print("Bad rabbitmq connection")
            self.connection = self._reconnect()


    def _open_connection(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
				credentials=pika.PlainCredentials(username=self.user, password=self.password),
				host=self.host,
				port=self.port,
				virtual_host=self.virtual_host
			))

        return connection

    def close_connection(self):
        try:
            self.connection.close()
        except Exception as e:
            print(e)

    def _get_channel(self, channel_number):
        return self.connection.channel(channel_number)

    def get_channel(self, channel_number):
        try:
            channel = self._get_channel(channel_number)
            print(channel)
            return channel
        except Exception as e:
            print(e)

    def _reconnect(self):
        for i in range(constants_reconnect.NUMBERS_TO_RECONNECT):
            try:
                connection = self._open_connection()
                return connection
            except:
                time.sleep(constants_reconnect.RECONNECT_TIMEOUT)
                print("reconnect rabbitmq")


