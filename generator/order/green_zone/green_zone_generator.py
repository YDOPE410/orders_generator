from generator.order.zone_generator import Generator_order_in_zone
from constant import constants_green_zone
from utils.random_between import random_between

class Generator_order_in_green_zone(Generator_order_in_zone):

    def set_status(self):
        self.result.status = constants_green_zone.LIST_STATUS_GREEN_ZONE[random_between(
                                                                    constants_green_zone.LEN_MIN_LIST_STATUS_GREEN_ZONE,
                                                                    constants_green_zone.LEN_MAX_LIST_STATUS_GREEN_ZONE,
                                                                    self.result.id)]