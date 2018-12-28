# -*- coding: utf-8 -*-

"""
pynata.template.rest_client
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Simple REST client with convenience features using requests library

:copyright: © 2018 Zsolt Mester
:license: MPL 2.0, see LICENSE for more details
"""

import requests


class RESTClientException(Exception):
    pass


class _RESTClient:
    def __init__(self):
        self._request_base_url = None
        self._request_options_template = None

    def _request(self, method, url, **kwargs):
        try:
            return True, requests.request(method, url, **kwargs)
        except requests.exceptions.RequestException as e:
            return False, str(e)


class RESTClient(_RESTClient):
    def __init__(self, base_url: str, **kwargs):
        _RESTClient.__init__(self)

        self.set_request_base_url(base_url)
        self.set_request_options_template(**kwargs.get('request_template', {}))

    def request(self, method: str, api_endpoint: str = '', **kwargs) -> requests.Response:
        """
        requests.request method wrapper

        :param method: request HTTP method
        :param api_endpoint: resource name to be appended to the base URL
        """
        request_url = self.setup_request_url(api_endpoint)
        request_options = self.setup_request_options(**kwargs)

        success, resp = self._request(method, request_url, **request_options)

        if not success:
            raise RESTClientException(resp)

        return resp

    def get(self, api_endpoint: str = '', **kwargs) -> requests.Response:
        """
        requests.get method wrapper

        :param api_endpoint: resource name to be appended to the base URL
        """
        return self.request('GET', api_endpoint=api_endpoint, **kwargs)

    def delete(self, api_endpoint: str = '', **kwargs) -> requests.Response:
        """
        requests.delete method wrapper

        :param api_endpoint: resource name to be appended to the base URL
        """
        return self.request('DELETE', api_endpoint=api_endpoint, **kwargs)

    def patch(self, api_endpoint: str = '', **kwargs) -> requests.Response:
        """
        requests.patch method wrapper

        :param api_endpoint: resource name to be appended to the base URL
        """
        return self.request('PATCH', api_endpoint=api_endpoint, **kwargs)

    def post(self, api_endpoint: str = '', **kwargs) -> requests.Response:
        """
        requests.post method wrapper

        :param api_endpoint: resource name to be appended to the base URL
        """
        return self.request('POST', api_endpoint=api_endpoint, **kwargs)

    def put(self, api_endpoint: str = '', **kwargs) -> requests.Response:
        """
        requests.put method wrapper

        :param api_endpoint: resource name to be appended to the base URL
        """
        return self.request('PUT', api_endpoint=api_endpoint, **kwargs)

    def options(self, api_endpoint: str = '', **kwargs) -> requests.Response:
        """
        requests.options method wrapper

        :param api_endpoint: resource name to be appended to the base URL
        """
        return self.request('OPTIONS', api_endpoint=api_endpoint, **kwargs)

    def format_response(self, success, data) -> dict:
        """
        Return uniform structure for responses

        example success: {'success': True, 'data': 'response data'}
        example failure: {'success': False, 'message': 'error message'}
        """
        return {'success': success, 'data': data} if success else {'success': success, 'message': data}

    def setup_request_url(self, api_endpoint: str = '') -> str:
        """Concatenate base url and api endpoint strings"""
        if not isinstance(api_endpoint, str):
            raise ValueError('invalid value for api_endpoint - {}'.format(api_endpoint))

        if api_endpoint.startswith('/'):
            api_endpoint = api_endpoint[1:]

        return '/'.join([self._request_base_url, api_endpoint]) if len(api_endpoint) > 0 else self._request_base_url

    def setup_request_options(self, **kwargs) -> dict:
        """
        Setup requests.request parameters for request
        Read request template configuration and expand it with any values received
        Template values are overridden if there is a matching parameter key name
        """

        if self._request_template is None:
            request_args = {}
        else:
            request_args = {k: v for k, v in self._request_template.items()}

        for k, v in kwargs.items():
            request_args[k] = v

        return request_args

    def set_request_base_url(self, base_url: str) -> None:
        """Configure base URL to be used for all requests"""
        if isinstance(base_url, str):
            self._request_base_url = base_url[:-1] if base_url.endswith('/') else base_url
        else:
            raise ValueError('invalid value for base_url - {}'.format(base_url))

    def set_request_options_template(self, **kwargs) -> None:
        """Configure common parameters that will be used for every request"""
        self._request_template = kwargs
