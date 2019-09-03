# -*- coding: utf-8 -*-

"""
pynata.logger.handler
~~~~~~~~~~~~~
Utility classes for Python built-in logging

:copyright: © 2019 Zsolt Mester
:license: MPL 2.0, see LICENSE for more details
"""

import logging
import logging.handlers
from typing import List, Union

from .common import LoggerCommon


class LoggerHandlerUtil(LoggerCommon):
    def __init__(self):
        LoggerCommon.__init__(self)

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
                c_kwargs = handler_kwargs.copy()
                log_level = c_kwargs.pop('log_level', 'warn')
                handler = self.get_handler(handler_type, **c_kwargs)

                self.set_handler_log_level(handler, log_level)
                handler.setFormatter(self.get_formatter())

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

    @staticmethod
    def get_handler(handler_type: str, **kwargs) -> logging.Handler:
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

    @staticmethod
    def remove_handler(logger: logging.Logger, handler: logging.Handler) -> None:
        """Remove and close handler found on Logger instance"""

        logger.removeHandler(handler)
        handler.close()

    def set_handler_log_level(self, handler: logging.Handler, log_level: Union[str, int, bool]) -> None:
        """Set handler logging level"""

        log_level = self.get_logging_level(log_level)
        handler.setLevel(log_level)
