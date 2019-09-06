# -*- coding: utf-8 -*-

"""
tests.logger.test_handler
~~~~~~~~~~~~~~~~~~~~~~~~~
Unittests for LoggerHandlerUtil class

:copyright: © 2019 Zsolt Mester
:license: MPL 2.0, see LICENSE for more details
"""

import logging
import logging.handlers

import pytest

from pynata.logger.logger import LoggerUtil
from pynata.logger.handler import LoggerHandlerUtil


@pytest.fixture(scope='class')
def log_util():
    return LoggerUtil()


@pytest.fixture(scope='class')
def log_handler_util():
    return LoggerHandlerUtil()


@pytest.fixture(scope='function')
def reset_logger(log_util):
    log_util.remove_logger(__name__)


@pytest.mark.usefixtures('reset_logger')
class TestAddHandler:
    def test_add_handler(self, log_handler_util):
        logger = logging.getLogger(__name__)

        assert len(logger.handlers) == 0

        handler = logging.StreamHandler()
        log_handler_util.add_handler(logger, handler)

        assert logger.handlers == [handler]

    def test_add_handler_list(self, log_handler_util):
        logger = logging.getLogger(__name__)

        assert len(logger.handlers) == 0

        handlers = [logging.StreamHandler(), logging.handlers.SysLogHandler()]
        log_handler_util.add_handler(logger, handlers)

        assert logger.handlers == handlers

    def test_add_handler_reset_handler(self, log_handler_util):
        logger = logging.getLogger(__name__)

        h1, h2 = logging.StreamHandler(), logging.StreamHandler()
        log_handler_util.add_handler(logger, [h1, h2], reset_handler=True)

        assert len(logger.handlers) == 1
        assert logger.handlers.pop() == h2

    def test_add_handler_no_reset_handler(self, log_handler_util):
        logger = logging.getLogger(__name__)

        h1, h2 = logging.StreamHandler(), logging.StreamHandler()
        log_handler_util.add_handler(logger, [h1, h2], reset_handler=False)

        assert logger.handlers == [h1, h2]


class TestGetHandler:
    def test_get_handler(self, log_handler_util, tmpdir):
        f = tmpdir.join('temp_file')

        assert isinstance(log_handler_util.get_handler('stream'), logging.StreamHandler)
        assert isinstance(log_handler_util.get_handler('file', filename=f), logging.FileHandler)
        assert isinstance(log_handler_util.get_handler('watchedfile', filename=f), logging.handlers.WatchedFileHandler)
        assert isinstance(log_handler_util.get_handler('rotatingfile', filename=f),
                          logging.handlers.RotatingFileHandler)
        assert isinstance(log_handler_util.get_handler('timedrotatingfile', filename=f),
                          logging.handlers.TimedRotatingFileHandler)
        assert isinstance(log_handler_util.get_handler('socket', host='x', port=0), logging.handlers.SocketHandler)
        assert isinstance(log_handler_util.get_handler('datagram', host='x', port=0), logging.handlers.DatagramHandler)
        assert isinstance(log_handler_util.get_handler('syslog'), logging.handlers.SysLogHandler)
        assert isinstance(log_handler_util.get_handler('nteventlog', appname='x'), logging.handlers.NTEventLogHandler)
        assert isinstance(log_handler_util.get_handler('smtp', mailhost='x', fromaddr='x', toaddrs='x', subject='x'),
                          logging.handlers.SMTPHandler)
        assert isinstance(log_handler_util.get_handler('memory', capacity='x'), logging.handlers.MemoryHandler)
        assert isinstance(log_handler_util.get_handler('http', host='x', url='x'), logging.handlers.HTTPHandler)
        assert isinstance(log_handler_util.get_handler('queue', queue='x'), logging.handlers.QueueHandler)

        with pytest.raises(ValueError):
            log_handler_util.get_handler('x')


class TestSetHandlerLevel:
    def test_set_handler_level(self, log_handler_util):
        handler = logging.StreamHandler()

        assert handler.level == 0

        log_handler_util.set_handler_log_level(handler, 50)

        assert handler.level == 50


class TestSetupHandlers:
    def test_setup_handlers_config_empty(self, log_handler_util):
        handlers_a = log_handler_util.setup_handlers({'stream': {}})
        handlers_b = log_handler_util.setup_handlers({'stream': []})
        handlers_c = log_handler_util.setup_handlers({'stream': ()})

        assert len(handlers_a) == len(handlers_b) == len(handlers_c) == 1

        h_a, h_b, h_c = handlers_a.pop(), handlers_b.pop(), handlers_c.pop()

        assert h_a.level == h_b.level == h_c.level == 0

    def test_setup_handlers_config_iterable(self, log_handler_util):
        handlers_a = log_handler_util.setup_handlers({'stream': [{'log_level': 'debug'}, {'log_level': 'info'}]})
        handlers_b = log_handler_util.setup_handlers({'stream': ({'log_level': 'debug'}, {'log_level': 'info'})})

        assert len(handlers_a) == len(handlers_b) == 2

        h1a, h2a = handlers_a
        h1b, h2b = handlers_b

        assert h1a.level == h1b.level == 10
        assert h2a.level == h2b.level == 20

        assert type(h1a) == type(h1b) == type(h2a) == type(h2b) == logging.StreamHandler

    def test_setup_handlers_config_boolean(self, log_handler_util):
        handlers_t = log_handler_util.setup_handlers(True)
        handlers_f = log_handler_util.setup_handlers(False)

        assert len(handlers_t) == len(handlers_f) == 1

        h_t, h_f = handlers_t.pop(), handlers_f.pop()

        assert isinstance(h_t, logging.StreamHandler) and h_t.level == 10
        assert isinstance(h_f, logging.StreamHandler) and h_f.level == 30


@pytest.mark.usefixtures('reset_logger')
class TestRemoveHandler:
    def test_remove_handler(self, log_handler_util):
        logger, handler = logging.getLogger(__name__), logging.StreamHandler()
        log_handler_util.add_handler(logger, handler)

        assert len(logger.handlers) == 1

        log_handler_util.remove_handler(logger, handler)

        assert len(logger.handlers) == 0
