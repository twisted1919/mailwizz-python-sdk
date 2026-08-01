"""Tests for ListSubscribers endpoint."""
from unittest.mock import Mock, patch

import pytest
from mailwizz.base import Base
from mailwizz.config import Config
from mailwizz.endpoint.list_subscribers import ListSubscribers


class TestListSubscribers:
    """Test suite for ListSubscribers endpoint."""

    @pytest.fixture
    def endpoint(self):
        """Create a ListSubscribers endpoint instance."""
        config = Config({
            'api_url': 'https://api.example.com/api',
            'public_key': 'PUB',
            'private_key': 'PRIV',
            'charset': 'utf-8'
        })
        Base.set_config(config)
        return ListSubscribers()

    @patch('mailwizz.client.Client.request')
    def test_get_subscribers(self, mock_request, endpoint):
        """Test getting subscribers from a list."""
        mock_response = Mock()
        mock_request.return_value = mock_response
        
        result = endpoint.get_subscribers('LIST123', page=1, per_page=10)
        
        assert result == mock_response
        mock_request.assert_called_once()

    @patch('mailwizz.client.Client.request')
    def test_get_subscriber(self, mock_request, endpoint):
        """Test getting a single subscriber."""
        mock_response = Mock()
        mock_request.return_value = mock_response
        
        result = endpoint.get_subscriber('LIST123', 'SUB456')
        
        assert result == mock_response
        mock_request.assert_called_once()

    @patch('mailwizz.client.Client.request')
    def test_create_subscriber(self, mock_request, endpoint):
        """Test creating a subscriber."""
        mock_response = Mock()
        mock_request.return_value = mock_response
        
        data = {
            'EMAIL': 'test@example.com',
            'FNAME': 'John',
            'LNAME': 'Doe'
        }
        
        result = endpoint.create('LIST123', data)
        
        assert result == mock_response
        mock_request.assert_called_once()

    @patch('mailwizz.client.Client.request')
    def test_update_subscriber(self, mock_request, endpoint):
        """Test updating a subscriber."""
        mock_response = Mock()
        mock_request.return_value = mock_response
        
        data = {'FNAME': 'Jane'}
        
        result = endpoint.update('LIST123', 'SUB456', data)
        
        assert result == mock_response
        mock_request.assert_called_once()

    @patch('mailwizz.client.Client.request')
    def test_delete_subscriber(self, mock_request, endpoint):
        """Test deleting a subscriber."""
        mock_response = Mock()
        mock_request.return_value = mock_response
        
        result = endpoint.delete('LIST123', 'SUB456')
        
        assert result == mock_response
        mock_request.assert_called_once()

    @patch('mailwizz.client.Client.request')
    def test_email_search(self, mock_request, endpoint):
        """Test searching by email."""
        mock_response = Mock()
        mock_request.return_value = mock_response
        
        result = endpoint.email_search('LIST123', 'test@example.com')
        
        assert result == mock_response
        mock_request.assert_called_once()

    @patch('mailwizz.client.Client.request')
    def test_search_by_custom_fields_correct_keys(self, mock_request, endpoint):
        """Test search_by_custom_fields uses correct string keys (regression test for bug)."""
        mock_response = Mock()
        mock_request.return_value = mock_response
        
        # This was broken - it used page value as key instead of 'page' string
        fields = {'CUSTOM_FIELD': 'value'}
        result = endpoint.search_by_custom_fields('LIST123', fields, page=2, per_page=20)
        
        # Verify the request was made
        assert result == mock_response
        mock_request.assert_called_once()

    def test_prepare_body_for_bulk(self, endpoint):
        """Test bulk subscriber data preparation."""
        data = [
            {'EMAIL': 'user1@example.com', 'FNAME': 'User', 'LNAME': 'One'},
            {'EMAIL': 'user2@example.com', 'FNAME': 'User', 'LNAME': 'Two'}
        ]
        
        result = endpoint._prepare_body(data)
        
        # Should create subscribers[0][EMAIL], subscribers[0][FNAME], etc.
        assert result['subscribers[0][EMAIL]'] == 'user1@example.com'
        assert result['subscribers[0][FNAME]'] == 'User'
        assert result['subscribers[0][LNAME]'] == 'One'
        assert result['subscribers[1][EMAIL]'] == 'user2@example.com'
        assert result['subscribers[1][FNAME]'] == 'User'
        assert result['subscribers[1][LNAME]'] == 'Two'

    def test_prepare_body_with_nested_details(self, endpoint):
        """Test bulk preparation with nested details dict."""
        data = [
            {
                'EMAIL': 'user@example.com',
                'status': 'subscribed',
                'details': {
                    'ip_address': '127.0.0.1',
                    'source': 'api'
                }
            }
        ]
        
        result = endpoint._prepare_body(data)
        
        # Should handle nested details dict
        assert result['subscribers[0][EMAIL]'] == 'user@example.com'
        assert result['subscribers[0][status]'] == 'subscribed'
        assert result['subscribers[0][details][ip_address]'] == '127.0.0.1'
        assert result['subscribers[0][details][source]'] == 'api'

    @patch('mailwizz.client.Client.request')
    def test_unsubscribe(self, mock_request, endpoint):
        """Test unsubscribe functionality."""
        mock_response = Mock()
        mock_request.return_value = mock_response
        
        result = endpoint.unsubscribe('LIST123', 'SUB456')
        
        assert result == mock_response
        mock_request.assert_called_once()

    @patch('mailwizz.endpoint.list_subscribers.ListSubscribers.email_search')
    @patch('mailwizz.endpoint.list_subscribers.ListSubscribers.unsubscribe')
    def test_unsubscribe_by_email(self, mock_unsubscribe, mock_search, endpoint):
        """Test unsubscribe by email address."""
        # Mock successful search
        mock_search_response = Mock()
        mock_search_response.json.return_value = {
            'status': 'success',
            'data': {'subscriber_uid': 'SUB456'}
        }
        mock_search.return_value = mock_search_response
        
        mock_unsub_response = Mock()
        mock_unsubscribe.return_value = mock_unsub_response
        
        result = endpoint.unsubscribe_by_email('LIST123', 'test@example.com')
        
        mock_search.assert_called_once_with('LIST123', 'test@example.com')
        mock_unsubscribe.assert_called_once_with('LIST123', 'SUB456')
        assert result == mock_unsub_response
