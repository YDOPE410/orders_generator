import json
from orders_generator.config.config_loader.config_loader import Config_loader
from orders_generator.config.configuration import Configuration
from orders_generator.config.mapper.mapper_from_dict import Mapper

class Json_config_loader(Config_loader):

    @staticmethod
    def load(json_path):
        try:
            with open(json_path, "r") as json_file:
                return json.load(json_file, object_hook=lambda dict: Mapper(dict))
        except Exception as e:
            print(f"{e}. Unable to load {json_path}")

    @staticmethod
    def write_default():
        config = Configuration()
        config.COUNT_ORDERS = 2000
        config.RED_ZONE = 0.15
        config.GREEN_ZONE = 0.6
        config.BLUE_ZONE = 0.25
        config.BATCH = 100
        config.MYSQL = Mapper({
            "DATABASE": "db_simcord_orders_history",
            "HOST": "localhost",
            "PORT": 3306,
            "PASSWORD": "",
            "USER": "hoffman"
        })
        config.RABBITMQ = Mapper({
            "HOST": "localhost",
            "PORT": 5672,
            "VIRTUAL_HOST": "/",
            "PASSWORD": "",
            "USER": "hoffman",
            "EXCHANGE": "orders_by_statuses"
        })
        config.LOG_TXT_FILE_PATH = "../logs/current_date.log"
        config.LOG_LVL = 1
        return config

