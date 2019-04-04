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


