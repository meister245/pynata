__version__ = '0.4.1'

from .logger import log_util


def setup_logger(logger_name, logger_level=None, handler_config=None, **kwargs):
    return log_util.setup_logger(logger_name, logger_level=logger_level, handler_config=handler_config, **kwargs)
