# -*- coding: utf-8 -*-

"""
tests.test_logger
~~~~~~~~~~~~~~~~~
Unittests for LoggerUtil class

:copyright: © 2018 Zsolt Mester
:license: MPL 2.0, see LICENSE for more details
"""

import logging

import pytest

from pynata.logger import LoggerUtil


@pytest.fixture(scope='class')
def log_util():
    return LoggerUtil()


@pytest.fixture(scope='function')
def reset_logger(log_util):
    log_util.remove_logger(__name__)


@pytest.mark.usefixtures('reset_logger')
class TestGetLogger:
    def test_get_logger_name(self, log_util):
        logger = log_util.get_logger(__name__)
        assert logger.name == __name__


class TestSetLogFormat:
    def test_get_logger_name(self, log_util):
        log_util.set_log_format('sample')
        assert log_util._log_format == 'sample'


class TestSetLogDateFormat:
    def test_get_logger_name(self, log_util):
        log_util.set_log_date_format('sample')
        assert log_util._log_date_format == 'sample'


@pytest.mark.usefixtures('reset_logger')
class TestSetLoggerLevel:
    def test_set_logger_level_type_logger_object(self, log_util):
        logger = log_util.get_logger(__name__)

        log_util.set_logger_level(logger, 50)
        assert logger.level == 50

    def test_set_logger_level_type_string(self, log_util):
        log_util.set_logger_level(__name__, 30)

        logger = log_util.get_logger(__name__)
        assert logger.level == 30


@pytest.mark.usefixtures('reset_logger')
class TestSetupLogger:
    def test_setup_logger_default(self, log_util):
        logger = log_util.setup_logger(__name__)

        assert isinstance(logger, logging.Logger)
        assert isinstance(logger.handlers.pop(), logging.NullHandler)
        assert logger.level == 0

    def test_setup_logger_custom_level(self, log_util):
        logger = log_util.setup_logger(__name__, logger_level=40)
        assert logger.level == 40

    def test_setup_logger_custom_handler(self, log_util):
        logger = log_util.setup_logger(__name__, handler_config={'stream': {}})
        assert isinstance(logger.handlers.pop(), logging.StreamHandler)

    def test_setup_logger_existing_no_override(self, log_util):
        log_util.setup_logger(__name__, logger_level=30)

        logger = log_util.setup_logger(__name__)
        assert logger.level == 30

    def test_setup_logger_existing_override_level(self, log_util):
        log_util.setup_logger(__name__, logger_level=30)

        logger = log_util.setup_logger(__name__, logger_level=50)
        assert logger.level == 50

    def test_setup_logger_existing_handler_no_reset(self, log_util):
        log_util.setup_logger(__name__)

        logger = log_util.setup_logger(__name__, reset_handler_type=False, remove_handlers=False)
        assert len(logger.handlers) == 2
        assert [type(h) for h in logger.handlers] == [logging.NullHandler, logging.NullHandler]


@pytest.mark.usefixtures('reset_logger')
class TestRemoveLogger:
    def test_remove_logger(self, log_util):
        log_util.setup_logger(__name__)
        assert log_util._logger_exists(__name__)

        log_util.remove_logger(__name__)
        assert log_util._logger_exists(__name__) is False


@pytest.mark.usefixtures('reset_logger')
class TestRemoveLoggers:
    def test_remove_loggers(self, log_util):
        log_util.setup_logger('logger1')
        log_util.setup_logger('logger2')

        assert log_util._logger_exists('logger1')
        assert log_util._logger_exists('logger2')

        log_util.remove_loggers()

        assert log_util._logger_exists('logger1') is False
        assert log_util._logger_exists('logger2') is False


@pytest.mark.usefixtures('reset_logger')
class TestRemoveLoggerHandlers:
    def test_remove_logger_handlers(self, log_util):
        logger = log_util.setup_logger(__name__)
        assert len(logger.handlers) != 0

        log_util.remove_logger_handlers(logger)
        assert len(logger.handlers) == 0
