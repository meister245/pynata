# -*- coding: utf-8 -*-

"""
tests.logger.test_logger
~~~~~~~~~~~~~~~~~~~~~~~~
Unittests for LoggerUtil class

:copyright: © 2019 Zsolt Mester
:license: MPL 2.0, see LICENSE for more details
"""

import logging

import pytest

from pynata.logger.logger import LoggerUtil


@pytest.fixture(scope='class')
def log_util():
    return LoggerUtil()


@pytest.fixture(scope='function')
def reset_logger(log_util):
    log_util.remove_logger(__name__)


@pytest.mark.usefixtures('reset_logger')
class TestGetLogger:
    def test_get_logger_name(self, log_util):
        logger_a = logging.getLogger(__name__)
        logger_b = log_util.get_logger(__name__)

        assert logger_a == logger_b and logger_b.name == __name__


class TestSetLogFormat:
    def test_set_log_msg_format(self, log_util):
        log_util.set_log_format('sample')

        assert log_util.log_format == 'sample'

    def test_set_log_date_format(self, log_util):
        log_util.set_log_date_format('sample')

        assert log_util.log_date_format == 'sample'


@pytest.mark.usefixtures('reset_logger')
class TestSetLoggerLevel:
    def test_set_logger_level(self, log_util):
        logger = log_util.get_logger(__name__)

        assert logger.level == 0

        log_util.set_logger_level(logger, 50)

        assert logger.level == 50

    def test_set_logger_level_string(self, log_util):
        log_util.set_logger_level(__name__, 30)
        logger = log_util.get_logger(__name__)

        assert logger.level == 30


@pytest.mark.usefixtures('reset_logger')
class TestSetupLogger:
    def test_setup_logger(self, log_util):
        logger_a = log_util.setup_logger(__name__)

        assert logger_a.level == 0 and len(logger_a.handlers) == 0

    def test_setup_logger_level(self, log_util):
        logger = log_util.setup_logger(__name__, logger_level=40)

        assert logger.level == 40 and len(logger.handlers) == 0

    def test_setup_logger_existing_override(self, log_util):
        logger_a = log_util.setup_logger(__name__, handler_config={'stream': {}})

        assert logger_a.level == 0 and len(logger_a.handlers) == 1

        logger_b = log_util.setup_logger(__name__)

        assert logger_a == logger_b
        assert len(logger_a.handlers) == len(logger_b.handlers) == 0

    def test_setup_logger_existing_no_override_handlers(self, log_util):
        logger_a = log_util.setup_logger(__name__, handler_config={'stream': {}})
        handler_a = logger_a.handlers[0]

        assert logger_a.level == 0 and len(logger_a.handlers) == 1

        logger_b = log_util.setup_logger(__name__, remove_handlers=False)

        assert logger_a == logger_b and len(logger_b.handlers) == 1

        handler_b = logger_b.handlers[0]

        assert handler_a == handler_b

    def test_setup_logger_existing_override_stream_handler(self, log_util):
        logger_a = log_util.setup_logger(__name__, handler_config={'stream': {}})
        handler_a = logger_a.handlers[0]

        logger_b = log_util.setup_logger(__name__, reset_handler_type=True,
                                         remove_handlers=False, handler_config={'stream': {}})

        assert logger_a == logger_b and len(logger_b.handlers) == 1
        assert logger_a.handlers[0] != handler_a

    def test_setup_logger_existing_no_override_stream_handler(self, log_util):
        logger_a = log_util.setup_logger(__name__, handler_config={'stream': {}})
        handler_a = logger_a.handlers[0]

        logger_b = log_util.setup_logger(__name__, remove_handlers=False, handler_config={'stream': {}})

        assert logger_a == logger_b and len(logger_b.handlers) == 2
        assert logger_a.handlers[0] == handler_a


@pytest.mark.usefixtures('reset_logger')
class TestLogging:
    def test_logging_notset(self, log_util, caplog):
        logger = log_util.setup_logger(__name__, handler_config={'stream': {}})

        assert logger.level == logger.handlers[0].level == 0

        logger.debug('test debug level')
        logger.warning('test warning level')

        assert [x.levelname for x in caplog.records] == ['DEBUG', 'WARNING']

    def test_logging_handler_log_level_higher(self, log_util, caplog):
        logger = log_util.setup_logger(__name__, logger_level=10, handler_config={'stream': {'log_level': 30}})

        assert logger.level == 10 and logger.handlers[0].level == 30

        logger.debug('test debug level')
        logger.warning('test warning level')

        assert [x.levelname for x in caplog.records] == ['DEBUG', 'WARNING']

    def test_logging_logger_log_level_higher(self, log_util, caplog):
        logger = log_util.setup_logger(__name__, logger_level=30, handler_config={'stream': {'log_level': 10}})

        assert logger.level == 30 and logger.handlers[0].level == 10

        logger.debug('test debug level')
        logger.warning('test warning level')

        assert [x.levelname for x in caplog.records] == ['WARNING']


@pytest.mark.usefixtures('reset_logger')
class TestRemoveLogger:
    def test_remove_logger(self, log_util):
        log_util.setup_logger(__name__)

        assert log_util.is_logger_exists(__name__)

        log_util.remove_logger(__name__)

        assert not log_util.is_logger_exists(__name__)


@pytest.mark.usefixtures('reset_logger')
class TestRemoveLoggers:
    def test_remove_loggers(self, log_util):
        log_util.setup_logger('logger1')
        log_util.setup_logger('logger2')

        assert log_util.is_logger_exists('logger1')
        assert log_util.is_logger_exists('logger2')

        log_util.remove_loggers()

        assert not log_util.is_logger_exists('logger1')
        assert not log_util.is_logger_exists('logger2')


@pytest.mark.usefixtures('reset_logger')
class TestRemoveLoggerHandlers:
    def test_remove_logger_handlers(self, log_util):
        logger = log_util.setup_logger(__name__, handler_config={'stream': {}})

        assert len(logger.handlers) == 1

        log_util.remove_logger_handlers(logger)

        assert len(logger.handlers) == 0
