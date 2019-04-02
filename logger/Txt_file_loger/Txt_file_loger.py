from datetime import datetime
from orders_generator.constant import constants_logger
from orders_generator.logger.logger import Logger
from orders_generator.decorator.singleton import singleton


@singleton
class Txt_file_logger(Logger):

    def __init__(self):
        self._log_lvl = 1
        self._txt_file_path = ""

    def set_txt_file_path(self, txt_file_path):
        self._txt_file_path = f"{txt_file_path[:txt_file_path.index('current_date')]}" \
           f"{str(datetime.now().strftime('%d-%m-%y'))}.log"\
                if 'current_date' in txt_file_path else txt_file_path
        print(f"Set new path to write log {txt_file_path}")

    def write_log(self, log_type, message):
        if self._log_lvl <= log_type:
            time = datetime.now()
            log = f"{time} : {constants_logger.LOG_TYPES[log_type]} : {message}\n"
            try:
                with open(self._txt_file_path, 'a') as txt_file:
                    txt_file.writelines(log)
            except Exception as e:
                print(f"{e}. Unable to write log.")