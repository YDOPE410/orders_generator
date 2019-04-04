from datetime import datetime
from orders_generator.constant import constants_logger
from orders_generator.logger.logger import Logger
from orders_generator.decorator.singleton import singleton
import os


@singleton
class Txt_file_logger(Logger):

    def __init__(self):
        self._log_lvl = 1
        self._txt_file_path = ""
        self._to_console = True

    def set_txt_file_path(self, txt_file_path):
        if not os.path.exists(txt_file_path[:txt_file_path.rfind('/')]):
            os.makedirs(txt_file_path[:txt_file_path.rfind('/')])
        self._txt_file_path = f"{txt_file_path[:txt_file_path.index('current_date')]}" \
           f"{str(datetime.now().strftime('%d-%m-%y'))}.log"\
                if 'current_date' in txt_file_path else txt_file_path
        print(f"Set new path to write log {txt_file_path}")

    def _write_log(self, log_type, message):
        if self._log_lvl <= log_type:
            time = datetime.now()
            log = f"{time} : {constants_logger.LOG_TYPES[log_type]} : {message}\n"
            if self._to_console:
                print(log)
            try:
                with open(self._txt_file_path, 'a') as txt_file:
                    txt_file.writelines(log)
            except Exception as e:
                print(f"{e}. Unable to write log.")

    def debug(self, message):
        self._write_log(constants_logger.DEBUG, message)

    def info(self, message):
        self._write_log(constants_logger.INFO, message)

    def warning(self, message):
        self._write_log(constants_logger.WARNING, message)

    def error(self, message):
        self._write_log(constants_logger.ERROR, message)

    def critical(self, message):
        self._write_log(constants_logger.CRITICAL, message)

    def fatal(self, message):
        self._write_log(constants_logger.DEBUG, message)