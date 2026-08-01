"""Tests for Request class and signing logic."""
import hashlib
import hmac
import urllib.parse
from collections import OrderedDict
from unittest.mock import Mock, patch

import pytest
from mailwizz.base import Base
from mailwizz.client import Client
from mailwizz.config import Config
from mailwizz.request import Request


class TestRequest:
    """Test suite for Request class."""

    def test_request_initialization(self):
        """Test request initialization with client."""
        client = Client({'url': 'https://api.example.com/test'})
        request = Request(client)
        
        assert request.client == client
        assert request.params == {}

    def test_request_instance_isolation(self):
        """Test that request instances don't share params dict."""
        client1 = Client({'url': 'https://api.example.com/test1'})
        client2 = Client({'url': 'https://api.example.com/test2'})
        
        request1 = Request(client1)
        request2 = Request(client2)
        
        request1.params['key1'] = 'value1'
        
        assert 'key1' not in request2.params

    @patch('mailwizz.request.time.time')
    def test_signature_generation_integer_timestamp(self, mock_time):
        """Test that timestamp is an integer (regression test for float bug)."""
        mock_time.return_value = 1234567890.123456
        
        config = Config({
            'api_url': 'https://api.example.com/api',
            'public_key': 'PUB123',
            'private_key': 'PRIV456',
            'charset': 'utf-8'
        })
        Base.set_config(config)
        
        client = Client({
            'url': 'https://api.example.com/api/lists',
            'method': 'POST',
            'params_post': {'name': 'Test List'}
        })
        
        request = Request(client)
        request._sign('https://api.example.com/api/lists')
        
        # Timestamp should be integer string
        timestamp = client.headers['X-MW-TIMESTAMP']
        assert timestamp == '1234567890'
        assert timestamp.isdigit()

    @patch('mailwizz.request.time.time')
    def test_signature_matches_php_style(self, mock_time):
        """Test that signature matches PHP SDK style (no trailing ampersand)."""
        mock_time.return_value = 1234567890.0
        
        config = Config({
            'api_url': 'https://api.example.com/api',
            'public_key': 'PUBLIC_KEY',
            'private_key': 'PRIVATE_KEY',
            'charset': 'utf-8'
        })
        Base.set_config(config)
        
        client = Client({
            'url': 'https://api.example.com/api/lists',
            'method': 'POST',
            'params_post': {'name': 'Test', 'description': 'Desc'}
        })
        
        request = Request(client)
        request._sign('https://api.example.com/api/lists')
        
        # Manually compute expected signature (PHP-style, no trailing &)
        params = {
            'X-MW-PUBLIC-KEY': 'PUBLIC_KEY',
            'X-MW-REMOTE-ADDR': '',
            'X-MW-TIMESTAMP': '1234567890',
            'name': 'Test',
            'description': 'Desc'
        }
        
        sorted_params = OrderedDict(sorted(params.items(), key=lambda kv: kv[0].lower()))
        encoded_parts = [
            urllib.parse.quote(str(k)) + '=' + urllib.parse.quote(str(v))
            for k, v in sorted_params.items()
        ]
        encoded_str = '&'.join(encoded_parts)
        
        signature_string = 'POST https://api.example.com/api/lists?' + encoded_str
        expected_signature = hmac.new(
            b'PRIVATE_KEY',
            signature_string.encode('utf-8'),
            hashlib.sha1
        ).hexdigest()
        
        assert client.headers['X-MW-SIGNATURE'] == expected_signature

    @patch('mailwizz.request.requests.get')
    def test_make_request_get(self, mock_get):
        """Test GET request execution."""
        mock_response = Mock()
        mock_get.return_value = mock_response
        
        client = Client({
            'url': 'https://api.example.com/api/lists',
            'method': 'GET',
            'params_get': {'page': '1', 'per_page': '10'}
        })
        
        request = Request(client)
        response = request._make_request()
        
        assert response == mock_response
        mock_get.assert_called_once_with(
            url='https://api.example.com/api/lists',
            params={'page': '1', 'per_page': '10'},
            headers=client.headers,
            timeout=30
        )

    @patch('mailwizz.request.requests.post')
    def test_make_request_post(self, mock_post):
        """Test POST request execution."""
        mock_response = Mock()
        mock_post.return_value = mock_response
        
        client = Client({
            'url': 'https://api.example.com/api/lists',
            'method': 'POST',
            'params_post': {'name': 'Test List'}
        })
        
        request = Request(client)
        response = request._make_request()
        
        assert response == mock_response
        mock_post.assert_called_once_with(
            url='https://api.example.com/api/lists',
            data={'name': 'Test List'},
            headers=client.headers,
            timeout=30
        )

    @patch('mailwizz.request.requests.put')
    def test_make_request_put(self, mock_put):
        """Test PUT request execution."""
        mock_response = Mock()
        mock_put.return_value = mock_response
        
        client = Client({
            'url': 'https://api.example.com/api/lists/ABC123',
            'method': 'PUT',
            'params_put': {'name': 'Updated List'}
        })
        
        request = Request(client)
        response = request._make_request()
        
        assert response == mock_response
        mock_put.assert_called_once_with(
            url='https://api.example.com/api/lists/ABC123',
            data={'name': 'Updated List'},
            headers=client.headers,
            timeout=30
        )

    @patch('mailwizz.request.requests.delete')
    def test_make_request_delete_uses_correct_params(self, mock_delete):
        """Test DELETE uses params_delete not params_put (regression test for bug)."""
        mock_response = Mock()
        mock_delete.return_value = mock_response
        
        client = Client({
            'url': 'https://api.example.com/api/lists/ABC123',
            'method': 'DELETE',
            'params_delete': {'confirm': 'yes'}
        })
        
        request = Request(client)
        response = request._make_request()
        
        assert response == mock_response
        mock_delete.assert_called_once_with(
            url='https://api.example.com/api/lists/ABC123',
            data={'confirm': 'yes'},  # Should be params_delete, not params_put
            headers=client.headers,
            timeout=30
        )

    @patch('mailwizz.request.requests.put')
    def test_send_adds_method_override_for_put(self, mock_put):
        """Test that PUT adds X-HTTP-Method-Override header."""
        mock_response = Mock()
        mock_put.return_value = mock_response
        
        config = Config({
            'api_url': 'https://api.example.com/api',
            'public_key': 'PUB',
            'private_key': 'PRIV',
            'charset': 'utf-8'
        })
        Base.set_config(config)
        
        client = Client({
            'url': 'https://api.example.com/api/lists/ABC123',
            'method': 'PUT',
            'params_put': {'name': 'Updated'}
        })
        
        request = Request(client)
        with patch('mailwizz.request.time.time', return_value=1234567890.0):
            request.send()
        
        assert client.headers.get('X-HTTP-Method-Override') == 'PUT'

    @patch('mailwizz.request.requests.delete')
    def test_send_adds_method_override_for_delete(self, mock_delete):
        """Test that DELETE adds X-HTTP-Method-Override header."""
        mock_response = Mock()
        mock_delete.return_value = mock_response
        
        config = Config({
            'api_url': 'https://api.example.com/api',
            'public_key': 'PUB',
            'private_key': 'PRIV',
            'charset': 'utf-8'
        })
        Base.set_config(config)
        
        client = Client({
            'url': 'https://api.example.com/api/lists/ABC123',
            'method': 'DELETE',
            'params_delete': {}
        })
        
        request = Request(client)
        with patch('mailwizz.request.time.time', return_value=1234567890.0):
            request.send()
        
        assert client.headers.get('X-HTTP-Method-Override') == 'DELETE'
