"""
Tests for User model.
"""
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from app.models.user import User


class TestUserModel:
    """Test cases for User model."""
    
    def test_user_creation(self):
        """Test creating a new user."""
        firebase_user_info = {
            'uid': 'test-user-123',
            'email': 'test@example.com',
            'name': 'Test User',
            'email_verified': True,
            'picture': 'https://example.com/avatar.jpg',
            'provider_id': 'google.com'
        }
        
        with patch('app.models.user.ndb') as mock_ndb:
            # Mock the put method
            mock_ndb.Model.put = MagicMock()
            
            user = User.create_from_firebase_user(firebase_user_info)
            
            assert user.uid == 'test-user-123'
            assert user.email == 'test@example.com'
            assert user.display_name == 'Test User'
            assert user.email_verified is True
            assert user.picture == 'https://example.com/avatar.jpg'
            assert user.provider_id == 'google.com'
            assert user.created_at is not None
            assert user.updated_at is not None
    
    def test_user_to_dict(self):
        """Test converting user to dictionary."""
        user = User(
            uid='test-user-123',
            email='test@example.com',
            display_name='Test User',
            email_verified=True,
            picture='https://example.com/avatar.jpg',
            provider_id='google.com'
        )
        
        # Mock datetime objects
        user.created_at = datetime(2023, 1, 1, 12, 0, 0)
        user.updated_at = datetime(2023, 1, 2, 12, 0, 0)
        
        user_dict = user.to_dict()
        
        assert user_dict['uid'] == 'test-user-123'
        assert user_dict['email'] == 'test@example.com'
        assert user_dict['display_name'] == 'Test User'
        assert user_dict['created_at'] == '2023-01-01T12:00:00'
        assert user_dict['updated_at'] == '2023-01-02T12:00:00'
        assert user_dict['email_verified'] is True
        assert user_dict['picture'] == 'https://example.com/avatar.jpg'
        assert user_dict['provider_id'] == 'google.com'
    
    def test_user_update_from_firebase(self):
        """Test updating user from Firebase data."""
        user = User(
            uid='test-user-123',
            email='old@example.com',
            display_name='Old Name',
            email_verified=False
        )
        
        firebase_user_info = {
            'uid': 'test-user-123',
            'email': 'new@example.com',
            'name': 'New Name',
            'email_verified': True,
            'picture': 'https://example.com/new-avatar.jpg',
            'provider_id': 'google.com'
        }
        
        with patch('app.models.user.ndb') as mock_ndb:
            # Mock the put method
            mock_ndb.Model.put = MagicMock()
            
            updated_user = user.update_from_firebase_user(firebase_user_info)
            
            assert updated_user.email == 'new@example.com'
            assert updated_user.display_name == 'New Name'
            assert updated_user.email_verified is True
            assert updated_user.picture == 'https://example.com/new-avatar.jpg'
            assert updated_user.provider_id == 'google.com'
    
    def test_get_by_uid(self):
        """Test getting user by UID."""
        with patch('app.models.user.ndb') as mock_ndb:
            # Mock the query method
            mock_query = MagicMock()
            mock_query.get.return_value = User(uid='test-user-123', email='test@example.com')
            mock_ndb.Model.query.return_value = mock_query
            
            user = User.get_by_uid('test-user-123')
            
            assert user.uid == 'test-user-123'
            assert user.email == 'test@example.com'
    
    def test_get_by_email(self):
        """Test getting user by email."""
        with patch('app.models.user.ndb') as mock_ndb:
            # Mock the query method
            mock_query = MagicMock()
            mock_query.get.return_value = User(uid='test-user-123', email='test@example.com')
            mock_ndb.Model.query.return_value = mock_query
            
            user = User.get_by_email('test@example.com')
            
            assert user.uid == 'test-user-123'
            assert user.email == 'test@example.com'
    
    def test_user_required_fields(self):
        """Test that required fields are properly set."""
        # Test that uid and email are required
        with pytest.raises(TypeError):
            User()  # Should fail without required fields
        
        # Test with required fields
        user = User(uid='test-user-123', email='test@example.com')
        assert user.uid == 'test-user-123'
        assert user.email == 'test@example.com' 