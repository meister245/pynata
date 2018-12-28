# -*- coding: utf-8 -*-

"""
tests.template.test_rest_client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unittests for RESTClient template class

:copyright: © 2018 Zsolt Mester
:license: MPL 2.0, see LICENSE for more details
"""

from pynata.template.rest_client import RESTClient, RESTClientException

import pytest
import requests


@pytest.fixture(scope='class')
def rest_client():
    return RESTClient(base_url='https://example.com/')


@pytest.fixture(scope='function')
def mock_requests(mocker):
    mocker.patch.object(requests, 'request')
    requests.request.return_value = 'ok'


@pytest.mark.usefixtures('mock_requests')
class TestRequestsMethods:
    def test_request_get(self, rest_client):
        r = rest_client.get(api_endpoint='/sample')
        requests.request.assert_called_with('GET', 'https://example.com/sample')
        assert r == 'ok'

    def test_request_post(self, rest_client):
        r = rest_client.post(api_endpoint='/sample')
        requests.request.assert_called_with('POST', 'https://example.com/sample')
        assert r == 'ok'

    def test_request_put(self, rest_client):
        r = rest_client.put(api_endpoint='/sample')
        requests.request.assert_called_with('PUT', 'https://example.com/sample')
        assert r == 'ok'

    def test_request_patch(self, rest_client):
        r = rest_client.patch(api_endpoint='/sample')
        requests.request.assert_called_with('PATCH', 'https://example.com/sample')
        assert r == 'ok'

    def test_request_delete(self, rest_client):
        r = rest_client.delete(api_endpoint='/sample')
        requests.request.assert_called_with('DELETE', 'https://example.com/sample')
        assert r == 'ok'

    def test_request_option(self, rest_client):
        r = rest_client.options(api_endpoint='/sample')
        requests.request.assert_called_with('OPTIONS', 'https://example.com/sample')
        assert r == 'ok'


class TestRequestsException:
    def test_requests_raises_exception(self, rest_client):
        rest_client.set_request_base_url('aaa')

        with pytest.raises(RESTClientException):
            rest_client.get()


class TestSetRequestBaseURL:
    def test_set_request_base_url(self, rest_client):
        rest_client.set_request_base_url('https://example.com/')
        assert rest_client._request_base_url == 'https://example.com'

        rest_client.set_request_base_url('https://example.com')
        assert rest_client._request_base_url == 'https://example.com'

    def test_set_request_base_url_raises_exception(self, rest_client):
        with pytest.raises(ValueError):
            rest_client.set_request_base_url(None)


class TestSetRequestOptionsTemplate:
    def test_set_request_options_template(self, rest_client):
        assert rest_client._request_template == {}

        params = {'key_a': 5, 'key_b': 'val_b'}
        rest_client.set_request_options_template(**params)
        assert rest_client._request_template == params

        rest_client.set_request_options_template(key_c=7, key_d='val_d')
        assert rest_client._request_template == {'key_c': 7, 'key_d': 'val_d'}


class TestSetupRequestURL:
    def test_setup_request_url(self, rest_client):
        url = rest_client.setup_request_url()
        assert url == rest_client._request_base_url

        url = rest_client.setup_request_url(api_endpoint='/sample')
        assert url == rest_client._request_base_url + '/sample'

        url = rest_client.setup_request_url(api_endpoint='sample')
        assert url == rest_client._request_base_url + '/sample'

    def test_setup_request_url_raises_exception(self, rest_client):
        with pytest.raises(ValueError):
            rest_client.setup_request_url(None)


class TestSetupRequestOptions:
    def test_setup_request_options(self, rest_client):
        options = rest_client.setup_request_options()
        assert options == {}

        options = rest_client.setup_request_options(params={'key_a': 2}, timeout=5)
        assert options == {'params': {'key_a': 2}, 'timeout': 5}

    def test_setup_request_options_with_template(self, rest_client):
        options = rest_client.setup_request_options()
        assert options == {}

        rest_client.set_request_options_template(timeout=5, verify=False)

        options = rest_client.setup_request_options()
        assert options == {'timeout': 5, 'verify': False}

        options = rest_client.setup_request_options(key_a=2)
        assert options == {'timeout': 5, 'verify': False, 'key_a': 2}

        # override template value
        options = rest_client.setup_request_options(timeout=3)
        assert options == {'timeout': 3, 'verify': False}
