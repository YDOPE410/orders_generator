import abc
from datetime import datetime
from generator.order.order import Order
from utils.linearly_congruential_method import LCM
from utils.random_between import random_between
from constant import constants_cur_pair, constants_description, constants_tag, constants_init_px, \
                                      constants_vol, constants_linearly_congruent_method, constants_date, \
                                      constants_direction, constants_timestamp


class Generator_order_in_zone(abc.ABC):
    result = Order()
    _LCM = LCM(constants_linearly_congruent_method.X0,
               constants_linearly_congruent_method.LCM_A,
               constants_linearly_congruent_method.LCM_C,
               constants_linearly_congruent_method.LCM_M)


    def set_id(self):
        self.result.id = self._LCM.next()


    def set_cur_pair(self):
        self.result.cur_pair = constants_cur_pair.LIST_CUR_PAIR[
            random_between(constants_cur_pair.LEN_MIN_LIST_CUR_PAIR,
                                          constants_cur_pair.LEN_MAX_LIST_CUR_PAIR,
                                          self.result.id)]

    def set_init_px(self):
        self.result.init_px = constants_init_px.LIST_INIT_PX[
            random_between(constants_init_px.LEN_MIN_LIST_INIT_PX,
                                          constants_init_px.LEN_MAX_LIST_INIT_PX,
                                          self.result.id)]

    def set_direction(self):
        self.result.direction = constants_direction.LIST_DIRECTION[
            random_between(constants_direction.LEN_MIN_LIST_DIRECTION,
                                          constants_direction.LEN_MAX_LIST_DIRECTION,
                                          self.result.id)]

    @abc.abstractmethod
    def set_status(self):
        pass

    def set_date(self):
        random_int = random_between(constants_timestamp.TIMESTAMP_MIN,
                                                   constants_timestamp.TIMESTAMP_MAX,
                                                   self.result.id)
        list_result = []
        if datetime.fromtimestamp(random_int / constants_date.ONE_SECOND_IN_MILLISECONDS).strftime("%w") == '6':
            timestamp = random_int - constants_date.ONE_DAY_IN_MILLISECONDS
        elif datetime.fromtimestamp(random_int / constants_date.ONE_SECOND_IN_MILLISECONDS).strftime("%w") == '7':
            timestamp = random_int + constants_date.ONE_DAY_IN_MILLISECONDS
        else:
            timestamp = random_int
        for i in range(len(self.result.status.split("->"))):
            timestamp += random_between(0, 3*constants_date.ONE_SECOND_IN_MILLISECONDS, self.result.id)
            list_result.append(str(timestamp))
        self.result.date = "->".join(list_result)

    def set_init_vol(self):
        self.result.init_vol = random_between(constants_vol.MIN_VOL,
                          constants_vol.MAX_VOL,
                          self.result.id)

    def set_description(self):
        self.result.description = constants_description.LIST_DESCRIPTION[random_between(
                                                           constants_description.LEN_MIN_LIST_DESCRIPTION,
                                                           constants_description.LEN_MAX_LIST_DESCRIPTION,
                                                           self.result.id)]

    def set_tag(self):
        self.result.tag = constants_tag.LIST_TAG[random_between(
                                                           constants_tag.LEN_MIN_LIST_TAG,
                                                           constants_tag.LEN_MAX_LIST_TAG,
                                                           self.result.id)]

    def set_fill_vol(self):
        last_status = self.result.status.split("->")[
            len(self.result.status.split("->")) - 1]
        if last_status == "fill":
            self.result.fill_vol = int(self.result.init_vol)
            return
        if last_status == "partial_fill":
            self.result.fill_vol = int(self.result.init_vol + self.result.init_vol / 100 *\
                                   random_between(-3, -1, self.result.id))
            return
        self.result.fill_vol = 0

    def set_fill_px(self):
        last_status = self.result.status.split("->")[
            len(self.result.status.split("->")) - 1]
        if last_status == "fill" or last_status == "partial_fill":
            self.result.fill_px = self.result.init_px + self.result.init_px / 100 *\
                                   random_between(-6, 6, self.result.id + 1)
            return
        self.result.fill_px = 0

    def generate(self):
        history_order = list()
        self.set_id()
        self.set_cur_pair()
        self.set_status()
        self.set_date()
        self.set_description()
        self.set_direction()
        self.set_init_px()
        self.set_init_vol()
        self.set_fill_px()
        self.set_fill_vol()
        self.set_tag()

        status_list = list()
        for status in self.result.status.split("->"):
            status_list.append(status)

        date_list = list()
        for date in self.result.date.split("->"):
            date_list.append(int(date))

        for i in range(len(date_list)):
            order = Order()
            order.status = status_list[i]
            order.date = date_list[i]
            order.id = self.result.id
            order.description = self.result.description
            order.tag = self.result.tag
            order.init_vol = self.result.init_vol
            order.init_px = self.result.init_px
            order.cur_pair = self.result.cur_pair
            order.direction = self.result.direction
            if order.status == "fill" or order.status == "partial_fill":
                order.fill_vol = self.result.fill_vol
                order.fill_px = self.result.fill_px
            else:
                order.fill_vol = 0
                order.fill_px = 0.0
            history_order.append(order)

        return history_order
