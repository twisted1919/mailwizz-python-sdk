"""Tests for Base class."""
import pytest
from mailwizz.base import Base
from mailwizz.config import Config


class TestBase:
    """Test suite for Base class."""

    def test_set_and_get_config(self):
        """Test setting and retrieving config."""
        config = Config({
            'api_url': 'https://api.example.com/api',
            'public_key': 'PUB',
            'private_key': 'PRIV',
            'charset': 'utf-8'
        })
        
        Base.set_config(config)
        
        base_instance = Base()
        assert base_instance.config == config

    def test_prepare_body_with_defaults(self):
        """Test _prepare_body method with default structure."""
        base = Base()
        
        data = {
            'general': {'name': 'Test', 'description': 'Desc'},
            'defaults': {'from_name': 'John'},
            'custom_key': 'custom_value'
        }
        
        result = base._prepare_body(data)
        
        # Should flatten nested dicts
        assert result['general[name]'] == 'Test'
        assert result['general[description]'] == 'Desc'
        assert result['defaults[from_name]'] == 'John'
        assert result['custom_key'] == 'custom_value'
        
        # Original keys should be removed
        assert 'general' not in result
        assert 'defaults' not in result

    def test_prepare_body_with_custom_default(self):
        """Test _prepare_body with custom default dict."""
        base = Base()
        
        data = {
            'subscriber': {'email': 'test@example.com', 'status': 'subscribed'}
        }
        
        default = {
            'subscriber': {},
            'metadata': {}
        }
        
        result = base._prepare_body(data, default)
        
        assert result['subscriber[email]'] == 'test@example.com'
        assert result['subscriber[status]'] == 'subscribed'

    def test_prepare_body_empty_data(self):
        """Test _prepare_body with empty data."""
        base = Base()
        
        result = base._prepare_body({})
        
        # Should still work, just no keys
        assert isinstance(result, dict)
