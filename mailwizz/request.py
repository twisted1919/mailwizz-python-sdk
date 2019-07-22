import html
import hashlib
import hmac
import os
import time
import requests
import urllib.parse

from collections import OrderedDict
from multidimensional_urlencode import urlencode
from mailwizz.base import Base


class Request(Base):
    """
    Request is the request class used to send the requests to the API endpoints.
    """

    client = None

    params = {}

    def __init__(self, client):
        self.client = client

    def send(self):
        """
        Send the request to the remote url.
        :return:
        """

        client = self.client
        get_params = client.params_get
        request_url = client.url.rstrip('/')

        if get_params:
            sorted_get_params = OrderedDict(sorted(get_params.items()))
            query_string = urlencode(sorted_get_params)

            if query_string:
                request_url += '?' + query_string

        self._sign(request_url)

        if client.is_put_method() or client.is_delete_method():
            client.headers['X-HTTP-Method-Override'] = client.method.upper()

        response = self._make_request()

        return response

    def _make_request(self):
        """
        Method that is making the request
        :return:
        """

        client = self.client

        if client.is_get_method():
            return requests.get(
                url=client.url,
                params=client.params_get,
                headers=client.headers,
                timeout=client.timeout
            )

        if client.is_post_method():
            return requests.post(
                url=client.url,
                data=client.params_post,
                headers=client.headers,
                timeout=client.timeout
            )

        if client.is_put_method():
            return requests.put(
                url=client.url,
                data=client.params_put,
                headers=client.headers,
                timeout=client.timeout
            )

        if client.is_delete_method():
            return requests.delete(
                url=client.url,
                data=client.params_put,
                headers=client.headers,
                timeout=client.timeout
            )

    def _sign(self, request_url):
        """
        Sign the request
        :param request_url:
        :return:
        """

        client = self.client
        config = self.config
        public_key = config.public_key
        private_key = config.private_key
        timestamp = time.time()

        remote_addr = ''
        if 'REMOTE_ADDR' in os.environ:
            remote_addr = html.escape(os.environ["REMOTE_ADDR"])

        headers = {
            'X-MW-PUBLIC-KEY': public_key,
            'X-MW-REMOTE-ADDR': remote_addr,
            'X-MW-TIMESTAMP': str(timestamp),
        }
        self.client.headers = headers

        params = {**headers, **client.params_post, **client.params_put, **client.params_delete}

        s = OrderedDict()
        for key in sorted(params, key=str.lower):
            s[key] = params[key]

        encoded_str = ''

        for key in s.keys():
            encoded_str += urllib.parse.quote(str(key)) + '=' + urllib.parse.quote(str(s[key])) + '&'

        encoded_str.rsplit('&')

        separator = '?'
        if len(client.params_get) > 0 and '?' in request_url:
            separator = '&'

        signature_string = client.method.upper() + ' ' + request_url + separator + encoded_str
        signature = hmac.new(
            bytes(private_key, config.charset),
            bytes(signature_string, config.charset),
            hashlib.sha1
        ).hexdigest()

        self.client.headers['X-MW-SIGNATURE'] = signature
