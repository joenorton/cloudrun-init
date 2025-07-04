"""
Firebase authentication utilities for cloudrun-init.
"""
import os
import functools
from flask import g, request, jsonify, current_app
import firebase_admin
from firebase_admin import auth, credentials
from google.auth.exceptions import GoogleAuthError


def init_firebase():
    """Initialize Firebase Admin SDK."""
    try:
        # Check if already initialized
        firebase_admin.get_app()
    except ValueError:
        # Initialize Firebase Admin SDK
        if os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY'):
            # Use service account key file
            cred = credentials.Certificate(os.environ['FIREBASE_SERVICE_ACCOUNT_KEY'])
            firebase_admin.initialize_app(cred)
        elif os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
            # Use default credentials
            firebase_admin.initialize_app()
        else:
            # For local development, try to initialize without credentials
            try:
                firebase_admin.initialize_app()
            except Exception as e:
                # If no credentials available, create a dummy app for testing
                current_app.logger.warning(f"Firebase initialization failed (this is OK for local development): {e}")
                current_app.logger.info("Firebase will not be available. Set FIREBASE_SERVICE_ACCOUNT_KEY for full functionality.")
                # Create a dummy app for testing
                firebase_admin.initialize_app(project_id='test-project')


def verify_firebase_token(id_token):
    """
    Verify Firebase ID token and return user info.
    
    Args:
        id_token (str): Firebase ID token from client
        
    Returns:
        dict: User information if token is valid, None otherwise
    """
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        
        # Extract user information
        user_info = {
            'uid': decoded_token['uid'],
            'email': decoded_token.get('email'),
            'email_verified': decoded_token.get('email_verified', False),
            'name': decoded_token.get('name'),
            'picture': decoded_token.get('picture'),
            'provider_id': decoded_token.get('firebase', {}).get('sign_in_provider', 'unknown')
        }
        
        return user_info
    except (ValueError, GoogleAuthError, auth.InvalidIdTokenError, auth.ExpiredIdTokenError) as e:
        current_app.logger.warning(f"Invalid Firebase token: {e}")
        return None


def get_token_from_request():
    """
    Extract Firebase ID token from request.
    
    Returns:
        str: ID token if found, None otherwise
    """
    # Check Authorization header
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header.split('Bearer ')[1]
    
    # Check for token in cookies
    token = request.cookies.get('firebase_token')
    if token:
        return token
    
    # Check for token in query parameters (for testing)
    token = request.args.get('token')
    if token:
        return token
    
    return None


def login_required(f):
    """
    Decorator to require Firebase authentication.
    
    Usage:
        @app.route('/protected')
        @login_required
        def protected_route():
            return jsonify({'user': g.user})
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # Initialize Firebase if not already done
        try:
            init_firebase()
        except Exception as e:
            current_app.logger.error(f"Failed to initialize Firebase: {e}")
            return jsonify({'error': 'Authentication service unavailable'}), 503
        
        # Get token from request
        token = get_token_from_request()
        if not token:
            return jsonify({'error': 'No authentication token provided'}), 401
        
        # Verify token
        user_info = verify_firebase_token(token)
        if not user_info:
            return jsonify({'error': 'Invalid or expired authentication token'}), 401
        
        # Attach user to Flask's g object
        g.user = user_info
        
        return f(*args, **kwargs)
    
    return decorated_function


def optional_login(f):
    """
    Decorator to optionally attach user if authenticated.
    
    Usage:
        @app.route('/optional-auth')
        @optional_login
        def optional_route():
            if g.user:
                return jsonify({'user': g.user})
            return jsonify({'message': 'No user logged in'})
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # Initialize Firebase if not already done
        try:
            init_firebase()
        except Exception as e:
            current_app.logger.error(f"Failed to initialize Firebase: {e}")
            # Continue without authentication
            g.user = None
            return f(*args, **kwargs)
        
        # Get token from request
        token = get_token_from_request()
        if token:
            # Verify token
            user_info = verify_firebase_token(token)
            if user_info:
                g.user = user_info
            else:
                g.user = None
        else:
            g.user = None
        
        return f(*args, **kwargs)
    
    return decorated_function 