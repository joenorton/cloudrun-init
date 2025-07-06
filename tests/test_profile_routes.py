"""
Tests for profile routes.
"""
import pytest
import json
from unittest.mock import patch, MagicMock
from app.models.user import User


class TestProfileRoutes:
    """Test cases for profile routes."""
    
    def test_get_profile_authenticated(self, client, mock_firebase_auth, mock_firebase_init):
        """Test getting profile when authenticated."""
        # Mock user model
        mock_user = User(
            uid='test-user-123',
            email='test@example.com',
            display_name='Test User',
            email_verified=True
        )
        mock_user.to_dict.return_value = {
            'uid': 'test-user-123',
            'email': 'test@example.com',
            'display_name': 'Test User',
            'email_verified': True
        }
        
        with patch('app.auth.user_middleware.get_or_create_user') as mock_get_user:
            mock_get_user.return_value = mock_user
            
            response = client.get('/profile/', headers={'Authorization': 'Bearer mock-token'})
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['user']['uid'] == 'test-user-123'
            assert data['message'] == 'Profile retrieved successfully'
    
    def test_get_profile_unauthenticated(self, client):
        """Test getting profile when not authenticated."""
        response = client.get('/profile/')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_update_profile_success(self, client, mock_firebase_auth, mock_firebase_init):
        """Test updating profile successfully."""
        # Mock user model
        mock_user = User(
            uid='test-user-123',
            email='test@example.com',
            display_name='Old Name',
            email_verified=True
        )
        mock_user.to_dict.return_value = {
            'uid': 'test-user-123',
            'email': 'test@example.com',
            'display_name': 'New Name',
            'email_verified': True
        }
        
        with patch('app.auth.user_middleware.get_or_create_user') as mock_get_user:
            mock_get_user.return_value = mock_user
            
            update_data = {'display_name': 'New Name'}
            response = client.put(
                '/profile/',
                data=json.dumps(update_data),
                content_type='application/json',
                headers={'Authorization': 'Bearer mock-token'}
            )
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['user']['display_name'] == 'New Name'
            assert data['message'] == 'Profile updated successfully'
    
    def test_update_profile_invalid_data(self, client, mock_firebase_auth, mock_firebase_init):
        """Test updating profile with invalid data."""
        # Mock user model
        mock_user = User(
            uid='test-user-123',
            email='test@example.com',
            display_name='Test User',
            email_verified=True
        )
        
        with patch('app.auth.user_middleware.get_or_create_user') as mock_get_user:
            mock_get_user.return_value = mock_user
            
            # Test with empty display name
            update_data = {'display_name': ''}
            response = client.put(
                '/profile/',
                data=json.dumps(update_data),
                content_type='application/json',
                headers={'Authorization': 'Bearer mock-token'}
            )
            
            assert response.status_code == 400
            data = json.loads(response.data)
            assert 'error' in data
            
            # Test with non-string display name
            update_data = {'display_name': 123}
            response = client.put(
                '/profile/',
                data=json.dumps(update_data),
                content_type='application/json',
                headers={'Authorization': 'Bearer mock-token'}
            )
            
            assert response.status_code == 400
            data = json.loads(response.data)
            assert 'error' in data
    
    def test_get_user_stats(self, client, mock_firebase_auth, mock_firebase_init):
        """Test getting user statistics."""
        from datetime import datetime
        
        # Mock user model
        mock_user = User(
            uid='test-user-123',
            email='test@example.com',
            display_name='Test User',
            email_verified=True,
            provider_id='google.com'
        )
        mock_user.created_at = datetime(2023, 1, 1, 12, 0, 0)
        mock_user.updated_at = datetime(2023, 1, 2, 12, 0, 0)
        
        with patch('app.auth.user_middleware.get_or_create_user') as mock_get_user:
            mock_get_user.return_value = mock_user
            
            response = client.get('/profile/stats', headers={'Authorization': 'Bearer mock-token'})
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'stats' in data
            assert data['stats']['email_verified'] is True
            assert data['stats']['provider'] == 'google.com'
            assert data['stats']['account_age_days'] is not None
    
    def test_sync_profile(self, client, mock_firebase_auth, mock_firebase_init):
        """Test syncing profile with Firebase data."""
        # Mock user model
        mock_user = User(
            uid='test-user-123',
            email='test@example.com',
            display_name='Test User',
            email_verified=True
        )
        mock_user.to_dict.return_value = {
            'uid': 'test-user-123',
            'email': 'test@example.com',
            'display_name': 'Test User',
            'email_verified': True
        }
        
        with patch('app.auth.user_middleware.get_or_create_user') as mock_get_user:
            mock_get_user.return_value = mock_user
            
            response = client.post('/profile/sync', headers={'Authorization': 'Bearer mock-token'})
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['user']['uid'] == 'test-user-123'
            assert data['message'] == 'Profile synced successfully'
    
    def test_profile_routes_require_authentication(self, client):
        """Test that profile routes require authentication."""
        routes = [
            ('GET', '/profile/'),
            ('PUT', '/profile/'),
            ('GET', '/profile/stats'),
            ('POST', '/profile/sync')
        ]
        
        for method, route in routes:
            if method == 'GET':
                response = client.get(route)
            elif method == 'PUT':
                response = client.put(route)
            elif method == 'POST':
                response = client.post(route)
            
            assert response.status_code == 401
            data = json.loads(response.data)
            assert 'error' in data 