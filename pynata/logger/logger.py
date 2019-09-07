# -*- coding: utf-8 -*-

"""
pynata.logger.logger
~~~~~~~~~~~~~
Utility classes for Python built-in logging

:copyright: © 2019 Zsolt Mester
:license: MPL 2.0, see LICENSE for more details
"""

import logging
import logging.handlers
from typing import Union

from .common import LoggerCommon
from .handler import LoggerHandlerUtil


class LoggerUtil(LoggerCommon):
    handler = LoggerHandlerUtil()

    def setup_logger(self, logger_name: str, logger_level: Union[str, int, bool] = None,
                     handler_config: Union[dict, bool] = None, **kwargs) -> logging.Logger:
        """
        Return a configured logging.Logger instance with logging handlers

        :param str logger_name: Logger object name
        :param str|int|bool logger_level: Logger object effective logging level - defaults to NOTSET
        :param dict handler_config: logging handlers to be created and added to the Logger - defaults to NullHandler

        :param bool remove_handlers: remove any existing handler on Logger object - defaults to True
        :param bool reset_handler_type: override existing handler type on Logger object - defaults to False

        """
        logger = self.get_logger(logger_name)

        if isinstance(logger_level, (str, int, bool)):
            self.set_logger_level(logger, self.get_logging_level(logger_level))

        if kwargs.get('remove_handlers', True):
            self.remove_logger_handlers(logger)

        for h in self.handler.setup_handlers(handler_config):
            self.handler.add_handler(logger, h, kwargs.get('reset_handler_type', False))

        return logger

    @staticmethod
    def get_logger(logger_name: str) -> logging.Logger:
        """Return logging.Logger instance, creates new instance if no instance exists by the given name"""

        return logging.getLogger(logger_name)

    def set_logger_level(self, logger: Union[str, logging.Logger], logger_level: Union[bool, int, str]) -> None:
        """Sets the logging level for a logging.Logger instance"""

        if isinstance(logger, str):
            logger = self.get_logger(logger)

        logger.setLevel(self.get_logging_level(logger_level))

    def remove_logger(self, logger_name: Union[str, logging.Logger]) -> None:
        """
        Deletes logging.Logger instance if found in logging.Logger.manager.loggerDict
        Removes and closes all handlers present on logging.Logger instance

        """
        if self.is_logger_exists(logger_name):
            self.remove_logger_handlers(logging.Logger.manager.loggerDict[logger_name])
            logging.Logger.manager.loggerDict.pop(logger_name)

    def remove_loggers(self) -> None:
        """
        Deletes all logging.Logger instances found in logging.Logger.manager.loggerDict
        Removes and closes all handlers present on logging.Logger instances

        """
        loggers = []

        for k, v in logging.Logger.manager.loggerDict.items():
            if isinstance(v, logging.Logger):
                loggers.append(k)
                self.remove_logger_handlers(v)

        for k in loggers:
            logging.Logger.manager.loggerDict.pop(k)

    def remove_logger_handlers(self, logger: logging.Logger) -> None:
        """Remove and close all handlers found on the logging.Logger instance"""

        for h in logger.handlers:
            self.handler.remove_handler(logger, h)
