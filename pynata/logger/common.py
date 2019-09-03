# -*- coding: utf-8 -*-

"""
pynata.logger.common
~~~~~~~~~~~~~
Utility classes for Python built-in logging

:copyright: © 2019 Zsolt Mester
:license: MPL 2.0, see LICENSE for more details
"""

import os
import logging
from typing import Union


class LoggerCommon:
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_date_format = '%Y-%m-%d %H:%M:%S'

    @staticmethod
    def get_default_logging_dir() -> str:
        """Return default OS specific home directory"""

        return os.path.expanduser('~')

    @classmethod
    def get_formatter(cls) -> logging.Formatter:
        """Return logging.Formatter instance"""

        return logging.Formatter(cls.log_format, cls.log_date_format)

    @staticmethod
    def get_logging_level(log_level: Union[str, int, bool]) -> int:
        """Return an integer for logging level configuration"""

        if isinstance(log_level, str) and isinstance(getattr(logging, log_level.upper(), 'invalid'), int):
            return getattr(logging, log_level.upper())

        elif isinstance(log_level, bool):
            return logging.DEBUG if log_level else logging.WARNING

        elif isinstance(log_level, int) and log_level in [0, 10, 20, 30, 40, 50]:
            return log_level

        else:
            raise ValueError('invalid logging level - {}'.format(log_level))

    @staticmethod
    def is_logger_exists(name: str) -> bool:
        """Return true if logging.Logger instance exists"""

        return True if name in logging.Logger.manager.loggerDict.keys() else False

    @classmethod
    def set_log_format(cls, format: str) -> None:
        """Sets the log record format that will be used with logging.Formatter instances"""

        if isinstance(format, str):
            cls.log_format = format

        else:
            raise ValueError('invalid type for log format string - {}'.format(format))

    @classmethod
    def set_log_date_format(cls, format_str: str) -> None:
        """Sets the log date record format that will be used with logging.Formatter instances"""

        if isinstance(format_str, str):
            cls.log_date_format = format_str

        else:
            raise ValueError('invalid type for log date format string - {}'.format(format_str))
