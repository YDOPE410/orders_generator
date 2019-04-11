from config.config_loader.json_config_loader.json_config_loader import Json_config_loader
from logger.Txt_file_loger.Txt_file_loger import Txt_file_logger
from service.database.database_connection.mysql_connection.mysql_connection import Mysql_connection
from service.database.service.mysql.mysql_service import Mysql_service
from service.message_broker.message_broker_connection.rabbitmq_connection.rabbitmq_connection import Rabbitmq_connection
from service.message_broker.service.rabbitmq.rabbitmq_service import Rabbitmq_service
from generator.order.order_generator import Order_generator
from generator.order.green_zone.green_zone_generator import Generator_order_in_green_zone
from generator.order.red_zone.red_zone_generator import Generator_order_in_red_zone
from generator.order.blue_zone.blue_zone_generator import Generator_order_in_blue_zone
from proto.serializer.order_serializer.order_serializer import Order_serializer
from constant import constants_format
from reporter.metric_storage.metric_storage import Metric_storage
from reporter.console_reporter.console_reporter import Console_reporter
from decorator.benchmark import benchmark
from constant import constants_logger


class Launcher:

    def _initialize(self):
        main_logger = Txt_file_logger()
        main_config = Json_config_loader.load("config_default.json")
        main_logger.set_txt_file_path(main_config.LOG_TXT_FILE_PATH)
        main_logger.set_log_lvl(constants_logger.DEBUG)
        metrics_storage = Metric_storage()
        main_rabbitmq_connection = Rabbitmq_connection(main_config.RABBITMQ.USER,
                                                       main_config.RABBITMQ.PASSWORD,
                                                       main_config.RABBITMQ.HOST,
                                                       main_config.RABBITMQ.VIRTUAL_HOST,
                                                       main_config.RABBITMQ.PORT)
        main_rabbitmq_connection.open_connection()
        main_rabbitmq = Rabbitmq_service(main_rabbitmq_connection)
        main_rabbitmq.add_publisher(1,
                                    "green_publisher",
                                    main_config.RABBITMQ.EXCHANGE_NAME,
                                    main_config.RABBITMQ.EXCHANGE_TYPE,
                                    "green_zone",
                                    main_config.RABBITMQ.ROUTING_KEY_GREEN_ZONE)
        main_rabbitmq.add_publisher(2,
                                    "red_publisher",
                                    main_config.RABBITMQ.EXCHANGE_NAME,
                                    main_config.RABBITMQ.EXCHANGE_TYPE,
                                    "red_zone",
                                    main_config.RABBITMQ.ROUTING_KEY_RED_ZONE)
        main_rabbitmq.add_publisher(3,
                                    "blue_publisher",
                                    main_config.RABBITMQ.EXCHANGE_NAME,
                                    main_config.RABBITMQ.EXCHANGE_TYPE,
                                    "blue_zone",
                                    main_config.RABBITMQ.ROUTING_KEY_BLUE_ZONE)
        main_database_connection = Mysql_connection(main_config.MYSQL.USER,
                                                    main_config.MYSQL.PASSWORD,
                                                    main_config.MYSQL.HOST,
                                                    main_config.MYSQL.PORT,
                                                    main_config.MYSQL.DATABASE)
        main_rabbitmq.add_consumer(4,
                                   "red_zone",
                                   "blue_zone")
        main_rabbitmq.add_consumer(5,
                                   "red_zone",
                                   "blue_zone")
        main_rabbitmq.add_consumer(6,
                                   "red_zone",
                                   "blue_zone")

        # for name in main_rabbitmq.consumers:
        #     print(name)
        #     main_rabbitmq.start_consume(name)

        main_database_connection.open_connection()
        main_mysql = Mysql_service(main_database_connection)

        return main_config, main_mysql, main_rabbitmq, main_logger,\
               main_database_connection, main_rabbitmq_connection, metrics_storage

    def _main(self, config, mysql, rabbitmq, logger,
                   database_connection, rabbitmq_connection):
        amount_red_zone = int(config.COUNT_ORDERS * config.RED_ZONE)
        amount_blue_zone = int(config.COUNT_ORDERS * config.BLUE_ZONE)
        amount_green_zone = int(config.COUNT_ORDERS * config.GREEN_ZONE)
        count_of_not_generate = config.COUNT_ORDERS - amount_blue_zone - amount_green_zone - amount_red_zone

        green_order_generator = Generator_order_in_green_zone()
        red_order_generator = Generator_order_in_red_zone()
        blue_order_generator = Generator_order_in_blue_zone()

        writed_lines = 0
        published = 0
        inserted_query = 0


        main_order_generator = Order_generator(red_order_generator)
        for gen in self._generate(main_order_generator, amount_red_zone, config):
            self._publish(gen, "red_publisher", rabbitmq)

        main_order_generator.change_zone(green_order_generator)
        for gen in self._generate(main_order_generator, amount_green_zone, config):
            self._publish(gen, "green_publisher", rabbitmq)

        main_order_generator.change_zone(blue_order_generator)
        for gen in self._generate(main_order_generator, amount_blue_zone, config):
            self._publish(gen, "blue_publisher", rabbitmq)



        logger.debug(f"{count_of_not_generate} orders can`t be generated")


    def _free(self, main_mysql_connection, main_rabbitmq_connection):
        main_mysql_connection.close_connection()
        main_rabbitmq_connection.close_connection()

    def _report(self, metrics):
        Console_reporter.write_report(data = metrics.storage)

    def start(self):
        main_config, main_mysql, main_rabbitmq, main_logger, \
        main_database_connection, main_rabbitmq_connection, metrics_storage  = self._initialize()
        self._main(main_config, main_mysql, main_rabbitmq, main_logger,
                   main_database_connection, main_rabbitmq_connection)
        self._report(metrics_storage)
        self._free(main_database_connection, main_rabbitmq_connection)

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
    def _publish(self, message, publisher_name, rabbitmq):
        rabbitmq.publishers[publisher_name].publish(Order_serializer.serialize(message))

    @benchmark
    def _insert_to_db(self, handler, value):
        if handler.execute(constants_format.INSERT_FORMAT.format(value)):
            return True
        return False

if __name__ == "__main__":
    launcher = Launcher()
    launcher.start()