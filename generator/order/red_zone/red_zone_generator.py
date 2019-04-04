from orders_generator.generator.order.zone_generator import Generator_order_in_zone
from orders_generator.constant import constants_red_zone
from orders_generator.utils.random_between import random_between

class Generator_order_in_red_zone(Generator_order_in_zone):

    def set_status(self):
        self.result.status = constants_red_zone.LIST_STATUS_RED_ZONE[random_between(
            constants_red_zone.LEN_MIN_LIST_STATUS_RED_ZONE,
            constants_red_zone.LEN_MAX_LIST_STATUS_RED_ZONE,
            self.result.id)]