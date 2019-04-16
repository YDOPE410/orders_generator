from config.config_loader.json_config_loader.json_config_loader import Json_config_loader
from logger.Txt_file_loger.Txt_file_loger import Txt_file_logger
from service.database.mysql.mysql import Mysql_service
from service.message_broker.rabbitmq.rabbitmq import Rabbitmq_service
from generator.order.order_generator import Order_generator
from generator.order.green_zone.green_zone_generator import Generator_order_in_green_zone
from generator.order.red_zone.red_zone_generator import Generator_order_in_red_zone
from generator.order.blue_zone.blue_zone_generator import Generator_order_in_blue_zone
from proto.serializer.order_serializer.order_serializer import Order_serializer
from service.storage.storage import Storage
from constant import constants_format
from reporter.metric_storage.metric_storage import Metric_storage
from reporter.console_reporter.console_reporter import Console_reporter
from decorator.benchmark import benchmark
from constant.constants_sql_queryes import REPORT
import time


class Launcher:

    def _initialize(self):
        storage = Storage()
        metrics = Metric_storage()
        config = Json_config_loader.load("config_default.json")
        logger = Txt_file_logger()
        logger.set_log_lvl(config.LOG_LVL)
        logger.set_txt_file_path(config.LOG_TXT_FILE_PATH)
        mysql = Mysql_service(config.MYSQL.USER, config.MYSQL.PASSWORD,
                              config.MYSQL.HOST, config.MYSQL.PORT, config.MYSQL.DATABASE)
        mysql.open_connection()
        rabbitmq = Rabbitmq_service(config.RABBITMQ.USER, config.RABBITMQ.PASSWORD, config.RABBITMQ.HOST,
                                    config.RABBITMQ.VIRTUAL_HOST, config.RABBITMQ.PORT)
        rabbitmq.open_connection()
        rabbitmq.add_publisher("red_publisher", config.RABBITMQ.EXCHANGE_NAME,
                               config.RABBITMQ.EXCHANGE_TYPE, "red_zone", config.RABBITMQ.ROUTING_KEY_RED_ZONE)
        rabbitmq.add_publisher("blue_publisher", config.RABBITMQ.EXCHANGE_NAME,
                               config.RABBITMQ.EXCHANGE_TYPE, "blue_zone", config.RABBITMQ.ROUTING_KEY_BLUE_ZONE)
        rabbitmq.add_publisher("green_publisher", config.RABBITMQ.EXCHANGE_NAME,
                               config.RABBITMQ.EXCHANGE_TYPE, "green_zone", config.RABBITMQ.ROUTING_KEY_GREEN_ZONE)

        rabbitmq.add_consumer("red_consumer", "red_zone")
        rabbitmq.add_consumer("blue_consumer", "blue_zone")
        rabbitmq.add_consumer("green_consumer", "green_zone")

        return config, mysql, rabbitmq, logger, storage, metrics

    def _main(self, config, mysql, rabbitmq, logger, storage):
        amount_red_zone = int(config.COUNT_ORDERS * config.RED_ZONE)
        amount_blue_zone = int(config.COUNT_ORDERS * config.BLUE_ZONE)
        amount_green_zone = int(config.COUNT_ORDERS * config.GREEN_ZONE)
        count_of_not_generate = config.COUNT_ORDERS - amount_blue_zone - amount_green_zone - amount_red_zone
        logger.debug(f"{count_of_not_generate} orders can`t be generated")

        green_order_generator = Generator_order_in_green_zone()
        red_order_generator = Generator_order_in_red_zone()
        blue_order_generator = Generator_order_in_blue_zone()

        main_order_generator = Order_generator(red_order_generator)
        for gen in self._generate(main_order_generator, amount_red_zone, config):
            self._publish(gen, "red_publisher", rabbitmq)

        main_order_generator.change_zone(green_order_generator)
        for gen in self._generate(main_order_generator, amount_green_zone, config):
            self._publish(gen, "green_publisher", rabbitmq)


        main_order_generator.change_zone(blue_order_generator)
        for gen in self._generate(main_order_generator, amount_blue_zone, config):
            self._publish(gen, "blue_publisher", rabbitmq)

        logger.debug("Start red_consumer")
        rabbitmq.consumers["red_consumer"].start()
        logger.debug("Start blue_consumer")
        rabbitmq.consumers["blue_consumer"].start()
        logger.debug("Start green_consumer")
        rabbitmq.consumers["green_consumer"].start()
        batch_count = int(storage.count()/config.BATCH)
        bath_amount = storage.count() - batch_count

        for i in range(batch_count):
            self._insert_batch_to_db(mysql, storage.pop(config.BATCH))

        self._insert_batch_to_db(mysql, storage.pop(bath_amount))



    @benchmark
    def _generate(self, generator, amount, config):
        count_of_batch = int(amount / config.BATCH)
        modulo = amount - count_of_batch * config.BATCH
        for i in range(count_of_batch):
            orders = generator.generate_batch(config.BATCH)
            for order in orders:
                yield order
        orders = generator.generate_batch(modulo)
        for order in orders:
            yield order

    @benchmark
    def _publish(self, message, publisher_name, rabbitmq):
        rabbitmq.publishers[publisher_name].publish(Order_serializer.serialize(message))

    @benchmark
    def _insert_to_db(self, handler, order):
        order = Order_serializer.deserialize(order)
        if handler.execute(constants_format.INSERT_FORMAT.format(order.id, order.cur_pair, order.direction,
                                                           order.status, order.date, order.init_px,order.fill_px,
                                                           order.init_vol, order.fill_vol, order.description, order.tag)):
            return True
        return False

    def _insert_batch_to_db(self, handler, batch):
        for order in batch:
            self._insert_to_db(handler, order)
        handler.commit()

    def _free(self, mysql, rabbitmq):
        mysql.close_connection()
        rabbitmq.close_connection()

    def _report(self, metrics, mysql, logger):
        Console_reporter.write_report(metrics.storage)
        report_from_sql = mysql.execute(REPORT)
        logger.debug(f"Orders count: {report_from_sql[0][0]}")
        logger.debug(f"Orders from green zone count: {report_from_sql[1][0]}")
        logger.debug(f"Orders from red zone count: {report_from_sql[2][0]}")
        logger.debug(f"Orders from blue zone count: {report_from_sql[3][0]}")
        #


    def start(self):
        config, mysql, rabbitmq, logger, storage, metrics = self._initialize()
        self._main(config, mysql, rabbitmq, logger, storage)
        self._report(metrics, mysql, logger)
        self._free(mysql, rabbitmq)


if __name__ == "__main__":
    launcher = Launcher()
    launcher.start()