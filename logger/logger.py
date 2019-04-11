import abc


class Logger(abc.ABC):


    _log_lvl = 1
    _to_console = True

    @abc.abstractmethod
    def _write_log(self, log_type, message):
        pass

    def console_handler(self, bool):
        if bool is True or bool is False:
            self._to_console = bool
        else:
            print("Console_handler takes bool parametr")

    def set_log_lvl(self, log_lvl):
        print(f"Change log_lvl from {self._log_lvl} to {log_lvl}")
        self._log_lvl = log_lvl
