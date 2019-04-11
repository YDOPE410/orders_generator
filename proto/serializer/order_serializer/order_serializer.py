from proto.serializer.serializer import Serializer
from proto.entity.order_pb2 import Order as Proto_order
from generator.order.order import Order

class Order_serializer(Serializer):
    @staticmethod
    def serialize(order):
        proto_order = Proto_order()
        proto_order.id = order.id
        proto_order.cur_pair = order.cur_pair
        proto_order.direction = order.direction
        proto_order.status = order.status
        proto_order.date = order.date
        proto_order.init_px = order.init_px
        proto_order.fill_px = order.fill_px
        proto_order.init_vol = order.init_vol
        proto_order.fill_vol = order.fill_vol
        proto_order.description = order.description
        proto_order.tag = order.tag

        serialized_order = proto_order.SerializeToString()

        return serialized_order
    @staticmethod
    def deserialize(order):
        proto_order = Proto_order()
        proto_order.ParseFromString(order)

        order = Order()
        order.id = proto_order.id
        order.cur_pair = proto_order.cur_pair
        order.direction = proto_order.direction
        order.status = proto_order.status
        order.date = proto_order.date
        order.init_px = proto_order.init_px
        order.fill_px = proto_order.fill_px
        order.init_vol = proto_order.init_vol
        order.fill_vol = proto_order.fill_vol
        order.description = proto_order.description
        order.tag = proto_order.tag

        return order