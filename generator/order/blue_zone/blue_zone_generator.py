from generator.order.zone_generator import Generator_order_in_zone
from constant import constants_blue_zone
from utils.random_between import random_between

class Generator_order_in_blue_zone(Generator_order_in_zone):

    def set_status(self):
        self.result.status = constants_blue_zone.LIST_STATUS_BLUE_ZONE[random_between(
                                                                constants_blue_zone.LEN_MIN_LIST_STATUS_BLUE_ZONE,
                                                                constants_blue_zone.LEN_MAX_LIST_STATUS_BLUE_ZONE,
                                                                self.result.id)]