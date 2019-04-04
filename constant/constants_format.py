INSERT_FORMAT = "insert into history(order_id, cur_pair, direction, status, date, init_px, fill_px, init_vol, " \
                "fill_vol, description, tag) values{0}"
ORDER_FORMAT = "({0}, '{1}', '{2}', '{3}', {4}, {5}, {6}, {7}, {8}, '{9}', '{10}')\n"
#0 - order id
#1 - order cur_pair
#2 - order direction
#3 - order status
#4 - order date
#5 - order init_px
#6 - order fill_px
#7 - order init_vol
#8 - order fill_vol
#9 - order description
#10 - order tag