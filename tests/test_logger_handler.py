# -*- coding: utf-8 -*-

"""
tests.test_logger_handler
~~~~~~~~~~~~~~~~~~~~~~~~~
Unittests for LoggerHandlerUtil class

:copyright: © 2018 Zsolt Mester
:license: MPL 2.0, see LICENSE for more details
"""

import logging
import logging.handlers

import pytest

from pynata.logger import LoggerUtil, LoggerHandlerUtil


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
        assert len(logger.handlers) == 1
        assert logger.handlers.pop() == handler

    def test_add_handler_list(self, log_handler_util):
        logger = logging.getLogger(__name__)
        assert len(logger.handlers) == 0

        handlers = [logging.StreamHandler(), logging.handlers.SysLogHandler()]
        log_handler_util.add_handler(logger, handlers)
        assert len(logger.handlers) == 2

        for x in handlers:
            assert x in logger.handlers

    def test_add_handler_reset_handler(self, log_handler_util):
        logger = logging.getLogger(__name__)

        h1 = logging.StreamHandler()
        h2 = logging.StreamHandler()
        log_handler_util.add_handler(logger, [h1, h2])

        assert len(logger.handlers) == 1
        assert logger.handlers.pop() == h2

    def test_add_handler_no_reset_handler(self, log_handler_util):
        logger = logging.getLogger(__name__)

        handlers = [logging.StreamHandler(), logging.handlers.SysLogHandler()]
        log_handler_util.add_handler(logger, handlers, reset_handler=False)

        assert len(logger.handlers) == 2

        for x in handlers:
            assert x in logger.handlers


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

        log_handler_util.set_handler_log_level(handler, 50)
        assert handler.level == 50


class TestSetupHandlers:
    def test_setup_handlers_default(self, log_handler_util):
        handlers = log_handler_util.setup_handlers()
        assert len(handlers) == 1
        assert isinstance(handlers.pop(), logging.NullHandler)

    def test_setup_handlers_basic_config(self, log_handler_util):
        handlers = log_handler_util.setup_handlers(config={'stream': {}})

        assert len(handlers) == 1

        h = handlers.pop()

        assert isinstance(h, logging.StreamHandler)
        assert h.level == 30

    def test_setup_handlers_custom_config(self, log_handler_util, tmpdir):
        config = {
            'syslog': {'log_level': 20},
            'stream': {'log_level': False},
            'file': {'log_level': 'critical', 'filename': tmpdir.join('temp_file')}
        }

        handlers = log_handler_util.setup_handlers(config)
        assert len(handlers) == 3

        h = [x for x in handlers if type(x) == logging.handlers.SysLogHandler].pop()
        assert h.level == 20

        h = [x for x in handlers if type(x) == logging.StreamHandler].pop()
        assert h.level == 30

        h = [x for x in handlers if type(x) == logging.FileHandler].pop()
        assert h.level == 50


@pytest.mark.usefixtures('reset_logger')
class TestRemoveHandler:
    def test_remove_handler(self, log_handler_util, tmpdir):
        logger = logging.getLogger(__name__)

        h = logging.FileHandler(filename=tmpdir.join('temp_file'))
        log_handler_util.add_handler(logger, h)
        assert len(logger.handlers) == 1
        assert getattr(h, 'stream', None)

        log_handler_util.remove_handler(logger, h)
        assert len(logger.handlers) == 0
        assert getattr(h, 'stream', None) is None
