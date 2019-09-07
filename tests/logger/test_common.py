# -*- coding: utf-8 -*-

"""
tests.logger.test_common
~~~~~~~~~~~~~~~~~~~~~~~~
Unittests for LoggerCommon class

:copyright: © 2019 Zsolt Mester
:license: MPL 2.0, see LICENSE for more details
"""

import logging

import pytest

from pynata.logger.common import LoggerCommon


@pytest.fixture(scope='class')
def log_common():
    return LoggerCommon()


class TestGetLoggingLevel:
    def test_get_logging_level(self, log_common):
        assert log_common.get_logging_level(30) == 30
        assert log_common.get_logging_level(None) == 0
        assert log_common.get_logging_level(True) == 10
        assert log_common.get_logging_level(False) == 30
        assert log_common.get_logging_level('warning') == 30

        with pytest.raises(ValueError):
            log_common.get_logging_level(300)

        with pytest.raises(ValueError):
            log_common.get_logging_level('invalid')


class TestLoggerExists:
    def test_logger_exist(self, log_common):
        assert not log_common.is_logger_exists(__name__)

        logging.getLogger(__name__)
        assert log_common.is_logger_exists(__name__)
