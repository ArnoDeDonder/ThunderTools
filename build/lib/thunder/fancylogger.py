import os
import sys
import logging

from colorama import Fore

from thunder.tools import get_current_formatted_datetime


_raise_error = os.environ.get('LOGGER_DIE_ON_ERROR', 'false').lower()
EXIT_ON_ERROR_LOGS = _raise_error == 'true'


class FancyLogsFormatter(logging.Formatter):
    level_colors = {
        logging.DEBUG: Fore.LIGHTWHITE_EX,
        logging.INFO: Fore.LIGHTBLUE_EX,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.LIGHTRED_EX
    }

    def format(self, record):
        formatted_message = f'{Fore.LIGHTBLACK_EX + get_current_formatted_datetime() + Fore.RESET} ' \
                            f'[{self.level_colors.get(record.levelno, "") + record.levelname + Fore.RESET}] ' \
                            f'{record.getMessage()}'
        return formatted_message


class FancyLogger:
    def __init__(self, default_log_level='INFO'):
        self._logger = logging.getLogger('thunder')
        if not self._logger.handlers:
            self._console_handler = logging.StreamHandler(sys.stdout)
            self._console_handler.setFormatter(FancyLogsFormatter())
            self._logger.addHandler(self._console_handler)
            self.set_log_level(default_log_level)

    @staticmethod
    def _parse_log_level(log_level):
        if log_level.upper() == 'DEBUG':
            return logging.DEBUG, 'DEBUG'
        elif log_level.upper() == 'INFO':
            return logging.INFO, 'INFO'
        elif log_level.upper() == 'WARNING':
            return logging.WARNING, 'WARNING'
        elif log_level.upper() == 'ERROR':
            return logging.ERROR, 'ERROR'
        elif log_level.upper() == 'CRITICAL':
            return logging.CRITICAL, 'CRITICAL'
        else:
            raise ValueError(f'{log_level} is an invalid log level. Valid: DEBUG/INFO/WARNING/ERROR/CRITICAL')
        
    @property
    def log_level(self):
        return self._log_level_name
    
    def set_log_level(self, log_level):
        self._log_level, self._log_level_name = self._parse_log_level(log_level)
        self._logger.setLevel(self._log_level)
        
    def log(self, message):
        self._logger.log(self._log_level, message)
        
    def debug(self, message):
        self._logger.debug(message)
        
    def info(self, message):
        self._logger.info(message)
        
    def warn(self, message):
        self._logger.warning(message)

    def warning(self, message):
        self.warn(message)
    
    def error(self, message):
        self._logger.error(message)
        if EXIT_ON_ERROR_LOGS:
            raise SystemExit(f'[ERROR EXIT]: {message}')
    
    def crit(self, message):
        self._logger.critical(message)
        if EXIT_ON_ERROR_LOGS:
            raise SystemExit(f'[CRITICAL EXIT]: {message}')

    def critical(self, message):
        self.crit(message)
        
        
def print(*args, sep=' ', end=None):
    global __PRINT_LOGGER__
    if '__PRINT_LOGGER__' not in globals():
        __PRINT_LOGGER__ = FancyLogger()
    if end:
        __PRINT_LOGGER__.warn('the end argument is not supported')
    __PRINT_LOGGER__.info(sep.join([str(val) for val in args]))
