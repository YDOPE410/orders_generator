from orders_generator.config.config_loader.json_config_loader.json_config_loader import Json_config_loader
from orders_generator.logger.Txt_file_loger.Txt_file_loger import Txt_file_logger
from orders_generator.service.db_service.mysql_service.mysql_service import Mysql_service
from orders_generator.service.message_broker.rabbitmq_service.rabbitmq_service import Rabbitmq_service
from orders_generator.service.file_service.txt_file_service.txt_file_service import Txt_file_service
from orders_generator.generator.order.order_generator import Order_generator
from orders_generator.generator.order.green_zone.green_zone_generator import Generator_order_in_green_zone
from orders_generator.generator.order.red_zone.red_zone_generator import Generator_order_in_red_zone
from orders_generator.generator.order.blue_zone.blue_zone_generator import Generator_order_in_blue_zone
from orders_generator.service.message_broker.publisher.rabbitmq_publisher.rabbitmq_publisher import Rabbitmq_publisher
from orders_generator.proto.serializer.order_serializer.order_serializer import Order_serializer
from orders_generator.constant import constants_format
from orders_generator.reporter.metric_storage.metric_storage import Metric_storage
from orders_generator.reporter.console_reporter.console_reporter import Console_reporter
from orders_generator.decorator.benchmark import benchmark


class Launcher:

    def _initialize(self):
        metrics_storage = Metric_storage()
        main_config = Json_config_loader.load("../config_default.json")
        main_logger = Txt_file_logger()
        main_logger.set_txt_file_path(main_config.LOG_TXT_FILE_PATH)
        main_logger.console_handler(main_config.CONSOLE_LOG)
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

        main_rabbitmq.exchange_declare(main_config.RABBITMQ.EXCHANGE_NAME, main_config.RABBITMQ.EXCHANGE_TYPE)

        main_rabbitmq.queue_declare(main_config.ZONE.BLUE_ZONE)
        main_rabbitmq.queue_declare(main_config.ZONE.RED_ZONE)
        main_rabbitmq.queue_declare(main_config.ZONE.GREEN_ZONE)

        main_rabbitmq.bind_queue(main_config.ZONE.BLUE_ZONE, main_config.RABBITMQ.EXCHANGE_NAME,
                                 main_config.RABBITMQ.ROUTING_KEY_BLUE_ZONE)
        main_rabbitmq.bind_queue(main_config.ZONE.RED_ZONE, main_config.RABBITMQ.EXCHANGE_NAME,
                                 main_config.RABBITMQ.ROUTING_KEY_RED_ZONE)
        main_rabbitmq.bind_queue(main_config.ZONE.GREEN_ZONE, main_config.RABBITMQ.EXCHANGE_NAME,
                                 main_config.RABBITMQ.ROUTING_KEY_RED_ZONE)

        txt_file = Txt_file_service(main_config.TXT_FILE_WITH_ORDERS, "a")
        txt_file.open_connection()
        return (main_config, main_mysql, main_rabbitmq, txt_file, main_logger, metrics_storage)

    def _main(self, main_config, main_mysql, main_rabbitmq, txt_file, logger):
        amount_red_zone = int(main_config.COUNT_ORDERS * main_config.RED_ZONE)
        amount_blue_zone = int(main_config.COUNT_ORDERS * main_config.BLUE_ZONE)
        amount_green_zone = int(main_config.COUNT_ORDERS * main_config.GREEN_ZONE)
        publisher = Rabbitmq_publisher(main_rabbitmq.get_channel())
        count_of_not_generate = main_config.COUNT_ORDERS - amount_blue_zone - amount_green_zone - amount_red_zone

        green_order_generator = Generator_order_in_green_zone()
        red_order_generator = Generator_order_in_red_zone()
        blue_order_generator = Generator_order_in_blue_zone()

        writed_lines = 0
        published = 0
        inserted_query = 0

        serializer = Order_serializer()

        main_order_generator = Order_generator(red_order_generator)
        for gen in self._generate(main_order_generator, amount_red_zone, main_config):
            if self._write_to_file(txt_file, gen):
                writed_lines += 1
            if self._publish(publisher,
                             gen,
                             main_config,
                             main_config.RABBITMQ.ROUTING_KEY_RED_ZONE,
                             serializer):
                published += 1

        main_order_generator.change_zone(green_order_generator)
        for gen in self._generate(main_order_generator, amount_green_zone, main_config):
            if self._write_to_file(txt_file, gen):
                writed_lines += 1
            if self._publish(publisher,
                             gen,
                             main_config,
                             main_config.RABBITMQ.ROUTING_KEY_GREEN_ZONE,
                             serializer):
                published += 1

        main_order_generator.change_zone(blue_order_generator)
        for gen in self._generate(main_order_generator, amount_blue_zone, main_config):
            if self._write_to_file(txt_file, gen):
                writed_lines += 1
            if self._publish(publisher,
                             gen,
                             main_config,
                             main_config.RABBITMQ.ROUTING_KEY_BLUE_ZONE,
                             serializer):
                published += 1
        txt_file.change_mod("r")
        for values in txt_file.read_all():
            if self._insert_to_db(main_mysql, values):
                inserted_query += 1
        main_mysql.commit()

        logger.debug(f"Writed lines {writed_lines}.")
        logger.debug(f"Published {published}.")
        logger.debug(f"Inserted queries {inserted_query}.")
        logger.debug(f"{count_of_not_generate} orders can`t be generated")


    def _free(self, main_mysql, main_rabbitmq, txt_file):
        main_mysql.close_connection()
        main_rabbitmq.close_connection()
        txt_file.close_connection()

    def _report(self, metrics):
        Console_reporter.write_report(data = metrics.storage)

    def start(self):
        conf, mysql, rabbitmq, file, logger, metrics = self._initialize()
        self._main(conf, mysql, rabbitmq, file, logger)
        self._report(metrics)
        self._free(mysql, rabbitmq, file)

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
    def _write_to_file(self, handler, message):
        if handler.write(str(message)):
            return True
        return False

    @benchmark
    def _publish(self, handler, message, config, rout_key, serializer):
        if handler.publish(config.RABBITMQ.EXCHANGE_NAME,
                          rout_key,
                          serializer.serialize(message)):
            return True
        return False

    @benchmark
    def _insert_to_db(self, handler, value):
        if handler.execute(constants_format.INSERT_FORMAT.format(value)):
            return True
        return False

if __name__ == "__main__":
    launcher = Launcher()
    launcher.start()