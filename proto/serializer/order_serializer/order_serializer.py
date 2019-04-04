from orders_generator.proto.serializer.serializer import Serializer
from orders_generator.proto.entity.order_pb2 import Order

class Order_serializer(Serializer):
    def serialize(self, order):
        proto_order = Order()
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

        serialized_order = str(proto_order.SerializeToString())

        return serialized_order