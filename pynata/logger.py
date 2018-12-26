# -*- coding: utf-8 -*-

"""
pynata.logger
~~~~~~~~~~~~~
Utility classes for Python built-in logging

:copyright: © 2018 Zsolt Mester
:license: MPL 2.0, see LICENSE for more details
"""

import logging
import logging.handlers
import os.path
from typing import List, Union


class _LoggerCommon:
    def __init__(self):
        self._log_format = None
        self._log_date_format = None

    def _get_default_logging_dir(self) -> str:
        """Return default OS specific home directory"""

        return os.path.expanduser('~')

    def _get_formatter(self) -> logging.Formatter:
        """Return logging.Formatter instance"""

        return logging.Formatter(self._log_format, self._log_date_format)

    def _get_logging_level(self, log_level: Union[str, int, bool]) -> int:
        """Return an integer for logging level configuration"""

        if isinstance(log_level, str) and isinstance(getattr(logging, log_level.upper(), 'invalid'), int):
            return getattr(logging, log_level.upper())

        elif isinstance(log_level, bool):
            return logging.DEBUG if log_level else logging.WARNING

        elif isinstance(log_level, int) and log_level in [0, 10, 20, 30, 40, 50]:
            return log_level

        else:
            raise ValueError('invalid logging level - {}'.format(log_level))

    def _logger_exists(self, name: str) -> bool:
        """Return if logging.Logger instance exists"""

        return True if name in logging.Logger.manager.loggerDict.keys() else False


class LoggerUtil(_LoggerCommon):
    def __init__(self, **kwargs):
        """
        :param str log_format: format string for logging records
        :param str log_date_format: date format string for logging records
        """

        _LoggerCommon.__init__(self)

        self.set_log_date_format(kwargs.get('log_date_format', '%Y-%m-%d %H:%M:%S'))
        self.set_log_format(kwargs.get('log_format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        self.handler_util = LoggerHandlerUtil()

    def setup_logger(self, logger_name: str, logger_level: Union[str, int, bool] = 'notset',
                     handler_config: Union[dict, None] = None, remove_handlers: bool = True,
                     reset_handler_type: bool = True) -> logging.Logger:
        """
        Return a configured logging.Logger instance with logging handlers

        :param str logger_name: Logger object name
        :param str|int|bool logger_level: Logger object effective logging level - defaults to NOTSET
        :param dict handler_config: logging handlers to be created and added to the Logger - defaults to NullHandler
        :param bool remove_handlers: remove any existing handler on Logger object - defaults to True
        :param bool reset_handler_type: override existing handler type on Logger object - defaults to True
        """

        logger = self.get_logger(logger_name)

        if self._get_logging_level(logger_level) != 0:
            self.set_logger_level(logger, logger_level)

        if remove_handlers:
            self.remove_logger_handlers(logger)

        for h in self.handler_util.setup_handlers(handler_config):
            self.handler_util.add_handler(logger, h, reset_handler_type)

        return logger

    def get_logger(self, logger_name: str) -> logging.Logger:
        """Return logging.Logger instance, creates new instance if no instance exists by the given name"""

        return logging.getLogger(logger_name)

    def set_log_format(self, format: str) -> None:
        """Sets the log record format that will be used with logging.Formatter instances"""

        if isinstance(format, str):
            self._log_format = format

        else:
            raise ValueError('invalid type for log format string - {}'.format(format))

    def set_log_date_format(self, format_str: str) -> None:
        """Sets the log date record format that will be used with logging.Formatter instances"""

        if isinstance(format_str, str):
            self._log_date_format = format_str

        else:
            raise ValueError('invalid type for log date format string - {}'.format(format_str))

    def set_logger_level(self, logger: Union[str, logging.Logger], logger_level: Union[bool, int, str]) -> None:
        """Sets the logging level for a logging.Logger instance"""

        if isinstance(logger, str):
            logger = self.get_logger(logger)

        logger.setLevel(self._get_logging_level(logger_level))

    def remove_logger(self, logger_name: Union[str, logging.Logger]) -> None:
        """
        Deletes logging.Logger instance if found in logging.Logger.manager.loggerDict
        Removes and closes all handlers present on logging.Logger instance
        """

        if self._logger_exists(logger_name):
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
            self.handler_util.remove_handler(logger, h)


class LoggerHandlerUtil(_LoggerCommon):
    def __init__(self):
        _LoggerCommon.__init__(self)

    def setup_handlers(self, config: Union[dict, None] = None) -> List[Union[logging.Handler, logging.NullHandler]]:
        """
        Returns a list of logging handler instances
        If no configuration is provided, a logging.NullHandler is returned

        :param dict config:
            defines logging handler instance(s) to be created
            dictionary key: defines handler type, key value: defines parameters for handler instance
            default logging level: "warning", can be overridden with "log_level"

            valid key names: 'stream', 'file', 'null', 'watchedfile', 'rotatingfile', 'timedrotatingfile', 'socket',
                'datagram', 'syslog', 'nteventlog', 'smtp', 'memory', 'http', 'queue'

            example: {
                "stream": {"log_level": "debug"},
                "file": {"filename": "/var/tmp/logfile", "log_level": "warning"},
                "rotatingfile": {"filename": "/var/tmp/logfile"}
            }
        """

        handlers = []

        if config is None:
            handlers.append(logging.NullHandler())

        elif isinstance(config, dict):
            for handler_type, handler_kwargs in config.items():
                log_level = handler_kwargs.pop('log_level', 'warn')
                handler = self.get_handler(handler_type, **handler_kwargs)

                self.set_handler_log_level(handler, log_level)
                handler.setFormatter(self._get_formatter())

                handlers.append(handler)

        else:
            raise ValueError('invalid type for config')

        return handlers

    def add_handler(self, logger: logging.Logger, handlers: Union[List[logging.Handler], logging.Handler],
                    reset_handler: bool = True) -> None:
        """
        Adds handler(s) to logging.Logger instance

        :param reset_handler: close existing Handler instance of the same class type on Logger instance
        """

        if not isinstance(handlers, list):
            handlers = [handlers]

        for h in handlers:
            if reset_handler:
                for x in [x for x in logger.handlers if type(x) == type(h)]:
                    self.remove_handler(logger, x)

            logger.addHandler(h)

    def get_handler(self, handler_type: str, **kwargs) -> logging.Handler:
        """logging.Handler factory method, returns a handler instance"""

        mapping = {
            'stream': logging.StreamHandler, 'file': logging.FileHandler, 'null': logging.NullHandler,
            'watchedfile': logging.handlers.WatchedFileHandler, 'rotatingfile': logging.handlers.RotatingFileHandler,
            'timedrotatingfile': logging.handlers.TimedRotatingFileHandler, 'socket': logging.handlers.SocketHandler,
            'datagram': logging.handlers.DatagramHandler, 'syslog': logging.handlers.SysLogHandler,
            'nteventlog': logging.handlers.NTEventLogHandler, 'smtp': logging.handlers.SMTPHandler,
            'memory': logging.handlers.MemoryHandler, 'http': logging.handlers.HTTPHandler,
            'queue': logging.handlers.QueueHandler
        }

        if isinstance(handler_type, str) and handler_type in mapping.keys():
            if handler_type in mapping.keys():
                return mapping[handler_type](**kwargs)
            else:
                raise ValueError('unknown handler class - {}'.format(handler_type))
        else:
            raise ValueError('invalid type for handler_type - {}'.format(handler_type))

    def remove_handler(self, logger: logging.Logger, handler: logging.Handler) -> None:
        """Remove and close handler found on Logger instance"""

        logger.removeHandler(handler)
        handler.close()

    def set_handler_log_level(self, handler: logging.Handler, log_level: Union[str, int, bool]) -> None:
        """Set handler logging level"""

        log_level = self._get_logging_level(log_level)
        handler.setLevel(log_level)
