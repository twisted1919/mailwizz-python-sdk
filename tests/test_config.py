"""Tests for Config class."""
import pytest
from mailwizz.config import Config


class TestConfig:
    """Test suite for Config class."""

    def test_config_initialization_with_dict(self):
        """Test config can be initialized with a dict."""
        config = Config({
            'api_url': 'https://api.example.com/api',
            'public_key': 'PUB123',
            'private_key': 'PRIV456',
            'charset': 'utf-8'
        })
        
        assert config.api_url == 'https://api.example.com/api/'
        assert config.public_key == 'PUB123'
        assert config.private_key == 'PRIV456'
        assert config.charset == 'utf-8'

    def test_config_api_url_normalization(self):
        """Test that API URL gets trailing slash."""
        config = Config({
            'api_url': 'https://api.example.com/api',
            'public_key': 'PUB',
            'private_key': 'PRIV',
            'charset': 'utf-8'
        })
        
        assert config.api_url.endswith('/')

    def test_config_invalid_url_no_scheme(self):
        """Test that invalid URL (no scheme) raises error."""
        with pytest.raises(ValueError, match="valid api base url"):
            Config({
                'api_url': 'api.example.com/api',
                'public_key': 'PUB',
                'private_key': 'PRIV',
                'charset': 'utf-8'
            })

    def test_config_invalid_url_no_netloc(self):
        """Test that invalid URL (no netloc) raises error."""
        with pytest.raises(ValueError, match="valid api base url"):
            Config({
                'api_url': 'https://',
                'public_key': 'PUB',
                'private_key': 'PRIV',
                'charset': 'utf-8'
            })

    def test_get_api_url(self):
        """Test endpoint URL construction."""
        config = Config({
            'api_url': 'https://api.example.com/api',
            'public_key': 'PUB',
            'private_key': 'PRIV',
            'charset': 'utf-8'
        })
        
        url = config.get_api_url('lists')
        assert url == 'https://api.example.com/api/lists'
        
        url = config.get_api_url('lists/ABC123/subscribers')
        assert url == 'https://api.example.com/api/lists/ABC123/subscribers'

    def test_get_api_url_without_base(self):
        """Test that get_api_url requires api_url to be set."""
        config = Config()
        
        with pytest.raises((ValueError, AttributeError)):
            config.get_api_url('lists')
