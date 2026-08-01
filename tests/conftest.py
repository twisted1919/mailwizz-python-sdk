"""Pytest configuration and fixtures."""
import pytest
from mailwizz.base import Base
from mailwizz.config import Config


@pytest.fixture
def config():
    """Provide a test configuration."""
    return Config({
        'api_url': 'https://api.example.com/api',
        'public_key': 'TEST_PUBLIC_KEY',
        'private_key': 'TEST_PRIVATE_KEY',
        'charset': 'utf-8'
    })


@pytest.fixture(autouse=True)
def reset_base_config():
    """Reset Base config before each test to ensure isolation."""
    Base.set_config(Config({
        'api_url': 'https://api.example.com/api',
        'public_key': 'TEST_PUBLIC_KEY',
        'private_key': 'TEST_PRIVATE_KEY',
        'charset': 'utf-8'
    }))
    yield
    # Reset after test
    Base.set_config({})
