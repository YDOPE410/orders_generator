from orders_generator.constant import constants_format


class Order:
    id = ""
    cur_pair = ""
    direction = ""
    status = ""
    date = 0
    init_px = 0.0
    fill_px = 0
    init_vol = 0.0
    fill_vol = 0
    description = ""
    tag = ""

    def __str__(self):
        return constants_format.ORDER_FORMAT.format(self.id,
                                                    self.cur_pair,
                                                    self.direction,
                                                    self.status,
                                                    self.date,
                                                    self.init_px,
                                                    self.fill_px,
                                                    self.init_vol,
                                                    self.fill_vol,
                                                    self.description,
                                                    self.tag)