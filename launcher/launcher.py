from orders_generator.config.config_loader.json_config_loader.json_config_loader import Json_config_loader
from orders_generator.logger.Txt_file_loger.Txt_file_loger import Txt_file_logger
import orders_generator.constant.constants_logger as log_lvl
from orders_generator.service.db_service.mysql_service.mysql_service import Mysql_service
from orders_generator.service.message_broker.rabbitmq_service.rabbitmq_service import Rabbitmq_service
from orders_generator.service.file_service.txt_file_service.txt_file_service import Txt_file_service
from orders_generator.generator.order.order_generator import Order_generator
from orders_generator.generator.order.green_zone.green_zone_generator import Generator_order_in_green_zone
from orders_generator.generator.order.red_zone.red_zone_generator import Generator_order_in_red_zone
from orders_generator.generator.order.blue_zone.blue_zone_generator import Generator_order_in_blue_zone
from orders_generator.service.message_broker.publisher.rabbitmq_publisher.rabbitmq_publisher import Rabbitmq_publisher


class Launcher:

    def _initialize(self):
        main_config = Json_config_loader.write_default()
        main_logger = Txt_file_logger()
        main_logger.set_txt_file_path(main_config.LOG_TXT_FILE_PATH)
        main_logger.set_log_lvl(log_lvl.ERROR)
        main_mysql = Mysql_service(main_config.MYSQL.USER,
                              main_config.MYSQL.PASSWORD,
                              main_config.MYSQL.HOST,
                              main_config.MYSQL.PORT,
                              main_config.MYSQL.DATABASE)
        main_mysql.open_connection()
        main_rabbitmq = Rabbitmq_service(main_config.RABBITMQ.USER,
                                         main_config.RABBITMQ.PASSWORD,
                                         main_config.RABBITMQ.HOST,
                                         main_config.RABBITMQ.VIRTUAL_HOST,
                                         main_config.RABBITMQ.PORT)
        main_rabbitmq.open_connection()
        txt_file = Txt_file_service("../resource/inserts.txt", "a")
        txt_file.open_connection()
        return (main_config, main_mysql, main_rabbitmq, txt_file)

    def _main(self, main_config, main_mysql, main_rabbitmq, txt_file):
        amount_red_zone = int(main_config.COUNT_ORDERS * main_config.RED_ZONE)
        amount_blue_zone = int(main_config.COUNT_ORDERS * main_config.BLUE_ZONE)
        amount_green_zone = int(main_config.COUNT_ORDERS * main_config.GREEN_ZONE)
        publisher = Rabbitmq_publisher(main_rabbitmq.get_channel())
        count_of_not_generate = main_config.COUNT_ORDERS - amount_blue_zone - amount_green_zone - amount_red_zone

        green_order_generator = Generator_order_in_green_zone()
        red_order_generator = Generator_order_in_red_zone()
        blue_order_generator = Generator_order_in_blue_zone()

        count_of_batch_green_zone = amount_green_zone / main_config.BATCH

        count_of_batch_blue_zone = amount_blue_zone / main_config.BATCH

        count_of_batch_red_zone = amount_red_zone / main_config.BATCH

        main_order_generator = Order_generator(green_order_generator)

        main_order_generator.change_zone(red_order_generator)

        main_order_generator.change_zone(blue_order_generator)


        print(f"{count_of_not_generate} orders can`t be generated")






    def _free(self, main_mysql, main_rabbitmq, txt_file):
        main_mysql.close_connection()
        main_rabbitmq.close_connection()
        txt_file.close_connection()

    def _report(self):
        pass

    def start(self):
        conf, mysql, rabbitmq, file = self._initialize()
        self._main(conf, mysql, rabbitmq, file)
        self._report()
        self._free(mysql, rabbitmq, file)


if __name__ == "__main__":
    launcher = Launcher()
    launcher.start()