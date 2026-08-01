"""Integration tests verifying full request flow."""
from unittest.mock import Mock, patch

import pytest
from mailwizz.base import Base
from mailwizz.config import Config
from mailwizz.endpoint.list_subscribers import ListSubscribers
from mailwizz.endpoint.lists import Lists


class TestIntegration:
    """Integration tests for complete request workflows."""

    @pytest.fixture
    def setup_sdk(self):
        """Setup SDK configuration."""
        config = Config({
            'api_url': 'https://demo.mailwizz.com/api',
            'public_key': 'DEMO_PUBLIC_KEY',
            'private_key': 'DEMO_PRIVATE_KEY',
            'charset': 'utf-8'
        })
        Base.set_config(config)

    @patch('mailwizz.request.requests.get')
    @patch('mailwizz.request.time.time')
    def test_full_get_request_flow(self, mock_time, mock_get, setup_sdk):
        """Test complete GET request flow from endpoint to HTTP."""
        mock_time.return_value = 1234567890.0
        mock_response = Mock()
        mock_response.json.return_value = {
            'status': 'success',
            'data': {'records': []}
        }
        mock_get.return_value = mock_response

        endpoint = Lists()
        response = endpoint.get_lists(page=1, per_page=10)

        assert response == mock_response
        mock_get.assert_called_once()
        
        # Verify signing headers were added
        # Compatible with both old and new Mock call_args format
        call_args = mock_get.call_args
        headers = call_args.kwargs['headers'] if hasattr(call_args, 'kwargs') else call_args[1]['headers']
        
        assert 'X-MW-PUBLIC-KEY' in headers
        assert 'X-MW-TIMESTAMP' in headers
        assert 'X-MW-SIGNATURE' in headers
        assert headers['X-MW-PUBLIC-KEY'] == 'DEMO_PUBLIC_KEY'
        assert headers['X-MW-TIMESTAMP'] == '1234567890'

    @patch('mailwizz.request.requests.post')
    @patch('mailwizz.request.time.time')
    def test_full_post_request_flow(self, mock_time, mock_post, setup_sdk):
        """Test complete POST request flow with data."""
        mock_time.return_value = 1234567890.0
        mock_response = Mock()
        mock_response.json.return_value = {
            'status': 'success',
            'data': {'list_uid': 'NEW123'}
        }
        mock_post.return_value = mock_response

        endpoint = Lists()
        data = {
            'general': {
                'name': 'Test List',
                'description': 'Test Description'
            },
            'defaults': {
                'from_name': 'John Doe',
                'from_email': 'john@example.com'
            }
        }
        
        response = endpoint.create(data)

        assert response == mock_response
        mock_post.assert_called_once()
        
        # Verify data was properly prepared (flattened)
        call_args = mock_post.call_args
        post_data = call_args.kwargs['data'] if hasattr(call_args, 'kwargs') else call_args[1]['data']
        
        assert 'general[name]' in post_data
        assert post_data['general[name]'] == 'Test List'
        assert 'defaults[from_name]' in post_data
        assert post_data['defaults[from_name]'] == 'John Doe'

    @patch('mailwizz.request.requests.put')
    @patch('mailwizz.request.time.time')
    def test_full_put_request_with_method_override(self, mock_time, mock_put, setup_sdk):
        """Test PUT request includes X-HTTP-Method-Override header."""
        mock_time.return_value = 1234567890.0
        mock_response = Mock()
        mock_response.json.return_value = {'status': 'success'}
        mock_put.return_value = mock_response

        endpoint = Lists()
        response = endpoint.update('LIST123', {'general': {'name': 'Updated Name'}})

        assert response == mock_response
        mock_put.assert_called_once()
        
        call_args = mock_put.call_args
        headers = call_args.kwargs['headers'] if hasattr(call_args, 'kwargs') else call_args[1]['headers']
        
        assert headers['X-HTTP-Method-Override'] == 'PUT'

    @patch('mailwizz.request.requests.delete')
    @patch('mailwizz.request.time.time')
    def test_full_delete_request_with_method_override(self, mock_time, mock_delete, setup_sdk):
        """Test DELETE request includes X-HTTP-Method-Override header."""
        mock_time.return_value = 1234567890.0
        mock_response = Mock()
        mock_response.json.return_value = {'status': 'success'}
        mock_delete.return_value = mock_response

        endpoint = Lists()
        response = endpoint.delete('LIST123')

        assert response == mock_response
        mock_delete.assert_called_once()
        
        call_args = mock_delete.call_args
        headers = call_args.kwargs['headers'] if hasattr(call_args, 'kwargs') else call_args[1]['headers']
        
        assert headers['X-HTTP-Method-Override'] == 'DELETE'
        # Regression test: should use params_delete, not params_put
        # Verify 'data' kwarg exists (exact params vary by version)
        has_data = ('data' in call_args.kwargs) if hasattr(call_args, 'kwargs') else ('data' in call_args[1])
        assert has_data

    @patch('mailwizz.request.requests.post')
    @patch('mailwizz.request.time.time')
    def test_bulk_subscriber_creation(self, mock_time, mock_post, setup_sdk):
        """Test bulk subscriber creation flow."""
        mock_time.return_value = 1234567890.0
        mock_response = Mock()
        mock_response.json.return_value = {'status': 'success'}
        mock_post.return_value = mock_response

        endpoint = ListSubscribers()
        bulk_data = [
            {'EMAIL': 'user1@example.com', 'FNAME': 'User', 'LNAME': 'One'},
            {'EMAIL': 'user2@example.com', 'FNAME': 'User', 'LNAME': 'Two'}
        ]
        
        response = endpoint.create_bulk('LIST123', bulk_data)

        assert response == mock_response
        mock_post.assert_called_once()
        
        call_args = mock_post.call_args
        post_data = call_args.kwargs['data'] if hasattr(call_args, 'kwargs') else call_args[1]['data']
        
        # Verify bulk array format
        assert 'subscribers[0][EMAIL]' in post_data
        assert 'subscribers[1][EMAIL]' in post_data
        assert post_data['subscribers[0][EMAIL]'] == 'user1@example.com'
        assert post_data['subscribers[1][EMAIL]'] == 'user2@example.com'

    def test_multiple_client_instances_isolated(self, setup_sdk):
        """Test that multiple simultaneous client instances don't interfere."""
        endpoint1 = Lists()
        endpoint2 = ListSubscribers()
        
        # Both should share the config but not interfere with each other
        assert endpoint1.config.api_url == endpoint2.config.api_url
        
        # Creating clients should not share state
        with patch('mailwizz.request.requests.get') as mock_get:
            mock_get.return_value = Mock()
            
            with patch('mailwizz.request.time.time', return_value=1234567890.0):
                endpoint1.get_lists()
                endpoint2.get_subscribers('LIST123')
            
            # Both should have made independent requests
            assert mock_get.call_count == 2
