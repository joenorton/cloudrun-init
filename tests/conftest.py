"""
Pytest configuration and fixtures for cloudrun-init.
"""
import pytest
import os
from unittest.mock import patch, MagicMock
from app.main import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to isolate the database for each test
    app = create_app({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key',
        'FIREBASE_PROJECT_ID': 'test-project',
        'GOOGLE_CLOUD_PROJECT': 'test-project'
    })

    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def mock_firebase_user():
    """Mock Firebase user data."""
    return {
        'uid': 'test-user-123',
        'email': 'test@example.com',
        'email_verified': True,
        'name': 'Test User',
        'picture': 'https://example.com/avatar.jpg',
        'provider_id': 'google.com'
    }


@pytest.fixture
def mock_firebase_token():
    """Mock Firebase ID token."""
    return 'mock-firebase-token-123'


@pytest.fixture
def authenticated_headers(mock_firebase_token):
    """Headers with authentication token."""
    return {'Authorization': f'Bearer {mock_firebase_token}'}


@pytest.fixture
def mock_firebase_auth():
    """Mock Firebase authentication."""
    with patch('app.auth.firebase.auth') as mock_auth:
        # Mock the verify_id_token method
        mock_auth.verify_id_token.return_value = {
            'uid': 'test-user-123',
            'email': 'test@example.com',
            'email_verified': True,
            'name': 'Test User',
            'picture': 'https://example.com/avatar.jpg',
            'firebase': {'sign_in_provider': 'google.com'}
        }
        yield mock_auth


@pytest.fixture
def mock_firebase_init():
    """Mock Firebase initialization."""
    with patch('app.auth.firebase.firebase_admin') as mock_firebase:
        # Mock the get_app method to raise ValueError (not initialized)
        mock_firebase.get_app.side_effect = ValueError("No app initialized")
        # Mock the initialize_app method
        mock_firebase.initialize_app.return_value = MagicMock()
        yield mock_firebase 