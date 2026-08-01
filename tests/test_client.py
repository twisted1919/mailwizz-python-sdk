"""Tests for Client class."""
import pytest
from mailwizz.client import Client


class TestClient:
    """Test suite for Client class."""

    def test_client_initialization_requires_url(self):
        """Test that Client requires a URL."""
        with pytest.raises(ValueError, match="Please set the url"):
            Client({})

    def test_client_default_method_is_get(self):
        """Test that default HTTP method is GET."""
        client = Client({'url': 'https://api.example.com/test'})
        assert client.method == Client.METHOD_GET
        assert client.is_get_method()

    def test_client_method_detection(self):
        """Test HTTP method detection methods."""
        # GET
        client = Client({'url': 'https://api.example.com/test', 'method': 'GET'})
        assert client.is_get_method()
        assert not client.is_post_method()
        assert not client.is_put_method()
        assert not client.is_delete_method()
        
        # POST
        client = Client({'url': 'https://api.example.com/test', 'method': 'POST'})
        assert client.is_post_method()
        assert not client.is_get_method()
        
        # PUT
        client = Client({'url': 'https://api.example.com/test', 'method': 'PUT'})
        assert client.is_put_method()
        
        # DELETE
        client = Client({'url': 'https://api.example.com/test', 'method': 'DELETE'})
        assert client.is_delete_method()

    def test_client_instance_isolation(self):
        """Test that client instances don't share state (regression test for bug)."""
        client1 = Client({
            'url': 'https://api.example.com/test1',
            'params_post': {'key1': 'value1'},
            'headers': {'X-Custom': 'header1'}
        })
        
        client2 = Client({
            'url': 'https://api.example.com/test2',
            'params_post': {'key2': 'value2'}
        })
        
        # Client 2 should not have client 1's data
        assert 'key1' not in client2.params_post
        assert client2.params_post.get('key2') == 'value2'
        assert 'X-Custom' not in client2.headers
        
        # Modify client1 after client2 creation
        client1.params_post['new_key'] = 'new_value'
        assert 'new_key' not in client2.params_post

    def test_client_parameters_initialization(self):
        """Test that all parameter types are properly initialized."""
        client = Client({
            'url': 'https://api.example.com/test',
            'params_get': {'get_key': 'get_val'},
            'params_post': {'post_key': 'post_val'},
            'params_put': {'put_key': 'put_val'},
            'params_delete': {'del_key': 'del_val'}
        })
        
        assert client.params_get == {'get_key': 'get_val'}
        assert client.params_post == {'post_key': 'post_val'}
        assert client.params_put == {'put_key': 'put_val'}
        assert client.params_delete == {'del_key': 'del_val'}

    def test_client_timeout_default(self):
        """Test default timeout value."""
        client = Client({'url': 'https://api.example.com/test'})
        assert client.timeout == 30

    def test_client_headers_initialization(self):
        """Test headers initialization."""
        client = Client({
            'url': 'https://api.example.com/test',
            'headers': {'Authorization': 'Bearer token'}
        })
        
        assert client.headers == {'Authorization': 'Bearer token'}
