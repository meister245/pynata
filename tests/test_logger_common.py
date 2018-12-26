# -*- coding: utf-8 -*-

"""
tests.test_logger_common
~~~~~~~~~~~~~~~~~~~~~~~~
Unittests for _LoggerCommon class

:copyright: © 2018 Zsolt Mester
:license: MPL 2.0, see LICENSE for more details
"""

import logging

import pytest

from pynata.logger import _LoggerCommon


@pytest.fixture(scope='class')
def log_common():
    return _LoggerCommon()


class TestGetDefaultLoggingDir:
    def test_get_default_logging_dir(self, log_common):
        assert isinstance(log_common._get_default_logging_dir(), str)


class TestGetFormatter:
    def test_get_formatter(self, log_common):
        assert isinstance(log_common._get_formatter(), logging.Formatter)


class TestGetLoggingLevel:
    def test_get_logging_level(self, log_common):
        assert log_common._get_logging_level(30) == 30
        assert log_common._get_logging_level(True) == 10
        assert log_common._get_logging_level(False) == 30
        assert log_common._get_logging_level('warning') == 30

        with pytest.raises(ValueError):
            log_common._get_logging_level(300)

        with pytest.raises(ValueError):
            log_common._get_logging_level('invalid')

        with pytest.raises(ValueError):
            log_common._get_logging_level(None)


class TestLoggerExists:
    def test_logger_exist(self, log_common):
        assert log_common._logger_exists(__name__) is False

        logging.getLogger(__name__)
        assert log_common._logger_exists(__name__)
