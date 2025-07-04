"""
Tests for authentication routes.
"""
import pytest
from unittest.mock import patch, MagicMock


class TestAuthRoutes:
    """Test authentication routes."""

    def test_health_endpoint(self, client):
        """Test the health endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'project' in data

    def test_version_endpoint(self, client):
        """Test the version endpoint."""
        response = client.get('/version')
        assert response.status_code == 200
        data = response.get_json()
        assert data['version'] == '0.1.0'
        assert data['phase'] == '0.1'

    def test_auth_status_unauthenticated(self, client):
        """Test auth status when not authenticated."""
        response = client.get('/auth/status')
        assert response.status_code == 200
        data = response.get_json()
        assert data['authenticated'] is False
        assert data['user'] is None

    @patch('app.auth.firebase.init_firebase')
    @patch('app.auth.firebase.verify_firebase_token')
    def test_auth_status_authenticated(self, mock_verify_token, mock_init_firebase, client, mock_firebase_user):
        """Test auth status when authenticated."""
        mock_verify_token.return_value = mock_firebase_user
        
        response = client.get('/auth/status?token=mock-token')
        assert response.status_code == 200
        data = response.get_json()
        assert data['authenticated'] is True
        assert data['user'] == mock_firebase_user

    def test_me_endpoint_no_token(self, client):
        """Test /me endpoint without authentication token."""
        response = client.get('/auth/me')
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    @patch('app.auth.firebase.init_firebase')
    @patch('app.auth.firebase.verify_firebase_token')
    def test_me_endpoint_with_valid_token(self, mock_verify_token, mock_init_firebase, client, mock_firebase_user):
        """Test /me endpoint with valid authentication token."""
        mock_verify_token.return_value = mock_firebase_user
        
        response = client.get('/auth/me?token=mock-token')
        assert response.status_code == 200
        data = response.get_json()
        assert data['authenticated'] is True
        assert data['user'] == mock_firebase_user

    @patch('app.auth.firebase.init_firebase')
    @patch('app.auth.firebase.verify_firebase_token')
    def test_me_endpoint_with_invalid_token(self, mock_verify_token, mock_init_firebase, client):
        """Test /me endpoint with invalid authentication token."""
        mock_verify_token.return_value = None
        
        response = client.get('/auth/me?token=invalid-token')
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_login_missing_token(self, client):
        """Test login endpoint with missing token."""
        response = client.post('/auth/login', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    @patch('app.auth.firebase.init_firebase')
    @patch('app.auth.firebase.verify_firebase_token')
    def test_login_with_valid_token(self, mock_verify_token, mock_init_firebase, client, mock_firebase_user):
        """Test login endpoint with valid token."""
        mock_verify_token.return_value = mock_firebase_user
        
        response = client.post('/auth/login', json={'idToken': 'valid-token'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Login successful'
        assert data['user'] == mock_firebase_user

    @patch('app.auth.firebase.init_firebase')
    @patch('app.auth.firebase.verify_firebase_token')
    def test_login_with_invalid_token(self, mock_verify_token, mock_init_firebase, client):
        """Test login endpoint with invalid token."""
        mock_verify_token.return_value = None
        
        response = client.post('/auth/login', json={'idToken': 'invalid-token'})
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_logout(self, client):
        """Test logout endpoint."""
        response = client.post('/auth/logout')
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Logout successful'

    def test_verify_token_missing_token(self, client):
        """Test token verification with missing token."""
        response = client.post('/auth/verify', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    @patch('app.auth.firebase.init_firebase')
    @patch('app.auth.firebase.verify_firebase_token')
    def test_verify_token_with_valid_token(self, mock_verify_token, mock_init_firebase, client, mock_firebase_user):
        """Test token verification with valid token."""
        mock_verify_token.return_value = mock_firebase_user
        
        response = client.post('/auth/verify', json={'idToken': 'valid-token'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['valid'] is True
        assert data['user'] == mock_firebase_user

    @patch('app.auth.firebase.init_firebase')
    @patch('app.auth.firebase.verify_firebase_token')
    def test_verify_token_with_invalid_token(self, mock_verify_token, mock_init_firebase, client):
        """Test token verification with invalid token."""
        mock_verify_token.return_value = None
        
        response = client.post('/auth/verify', json={'idToken': 'invalid-token'})
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data


class TestFirebaseAuth:
    """Test Firebase authentication utilities."""

    @patch('app.auth.firebase.firebase_admin')
    def test_init_firebase_with_service_account(self, mock_firebase_admin):
        """Test Firebase initialization with service account key."""
        with patch.dict('os.environ', {'FIREBASE_SERVICE_ACCOUNT_KEY': '/path/to/key.json'}):
            from app.auth.firebase import init_firebase
            mock_firebase_admin.get_app.side_effect = ValueError("No app initialized")
            
            init_firebase()
            
            mock_firebase_admin.initialize_app.assert_called_once()

    @patch('app.auth.firebase.firebase_admin')
    def test_init_firebase_with_default_credentials(self, mock_firebase_admin):
        """Test Firebase initialization with default credentials."""
        with patch.dict('os.environ', {'GOOGLE_APPLICATION_CREDENTIALS': '/path/to/credentials.json'}):
            from app.auth.firebase import init_firebase
            mock_firebase_admin.get_app.side_effect = ValueError("No app initialized")
            
            init_firebase()
            
            mock_firebase_admin.initialize_app.assert_called_once()

    def test_get_token_from_request_authorization_header(self, client):
        """Test token extraction from Authorization header."""
        from app.auth.firebase import get_token_from_request
        
        with client.test_request_context('/', headers={'Authorization': 'Bearer test-token'}):
            token = get_token_from_request()
            assert token == 'test-token'

    def test_get_token_from_request_cookie(self, client):
        """Test token extraction from cookie."""
        from app.auth.firebase import get_token_from_request
        
        with client.test_request_context('/', headers={'Cookie': 'firebase_token=test-token'}):
            token = get_token_from_request()
            assert token == 'test-token'

    def test_get_token_from_request_query_param(self, client):
        """Test token extraction from query parameter."""
        from app.auth.firebase import get_token_from_request
        
        with client.test_request_context('/?token=test-token'):
            token = get_token_from_request()
            assert token == 'test-token' 